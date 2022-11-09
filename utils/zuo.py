import hashlib
import pickle
import secrets
import math
import random
import os
from Crypto.Cipher import AES

def gen_bitmap(db_list, fileid_list, bslength):
  # bslength means the length of bitmap, that is the number of files.
  bs_list = ["0" for x in range(bslength)]
  for fileid in fileid_list:
    bs_list[db_list.get(fileid)] = "1"
  bs_string = ''.join(bs_list)
  return int(bs_string, 2).to_bytes(int(bslength / 8), byteorder="big")

def primitive_hash_h(msg):
  m= hashlib.sha256()
  m.update(msg)
  hash_msg = m.digest()
  return hash_msg

def pseudo_permutation_P(key, raw, iv):
  cipher = AES.new(key,AES.MODE_CBC,iv) #raw must be multiple of 16
  return cipher.encrypt(raw)

def pseudo_inverse_permutation_P(key, ctext,iv):
  cipher = AES.new(key,AES.MODE_CBC,iv)
  return cipher.decrypt(ctext)

class Zuo(object):
  """docstring for zuo
  dbfile: string, the path of db file
  bslength: the lenght of bitmap
  """
  def __init__(self, dbfile, bslength):
    with open(dbfile, 'rb') as f:
      self.db = pickle.load(f)
    self.bslength = bslength
    self.tokens = []
    self.keyword_list = [k for k in self.db.keys()]
    self.keyword_list.sort()
    self.tree_height = math.ceil(math.log(len(self.keyword_list), 2))

    self.K = os.urandom(16)
    self.iv = os.urandom(16)
    self.msg = primitive_hash_h(bytes("test", "utf-8"))
    self.C = pseudo_permutation_P(self.K, self.msg, self.iv)

  def gen_edb(self):
    self.expand_keyword = []
    self.expand_db = {}
    for i in range(self.tree_height, -1, -1): # 树节点的数量： 2 ** (height + 1) - 1
      for j in range(2 ** i):
        temp_keyword = bin(j)[2:].rjust(i + 1, "0")
        if i == self.tree_height:
          self.expand_db.setdefault(temp_keyword, self.db.get(self.keyword_list[j], set()))
        else:
          temp_fileid = self.expand_db.get(f"{temp_keyword}0") | self.expand_db.get(f"{temp_keyword}1")
          self.expand_db.setdefault(temp_keyword, temp_fileid)
    # 开始构建对应的 bitmap 与 edb
    self.edb = {}
    file_posi = {}
    file_list = list(self.expand_db.get("0"))
    for i, j in enumerate(file_list):
      file_posi.setdefault(j, i)
    for keyword in self.expand_db.keys():
      bs = gen_bitmap(file_posi, self.expand_db.get(keyword), self.bslength)
      # 补一个加密 bs
      # 补一个加密 keyword
      self.edb.setdefault(keyword, bs)
    self.edb.setdefault("file_index", file_list)

  def gen_localtree(self):
    pass

  def gen_token(self, query_range):
    (left_node, right_node) = [bin(self.keyword_list.index(x))[2:].rjust(self.tree_height + 1, "0") for x in query_range]
    BRC_nodes = []
    # self.keyword_list.index(query_range[0])
    # self.keyword_list.index(query_range[1])
    i = self.tree_height
    while int(left_node, 2) < int(right_node, 2):
      if left_node[-1] == "1":
        BRC_nodes.append(left_node)
      if right_node[-1] == "0":
        BRC_nodes.append(right_node)
      left_node = bin(int(left_node, 2) + 1)[2:].rjust(i, "0")[:-1]
      right_node = bin(int(right_node, 2) - 1)[2:].rjust(i, "0")[:-1]    
      i -= 1
    if left_node == right_node:
      BRC_nodes.append(left_node)
    # print(BRC_nodes)
    return BRC_nodes

  def search(self, token_list):
    search_result = []
    for token in token_list:
      search_result.append(self.edb.get(token))
    return search_result

