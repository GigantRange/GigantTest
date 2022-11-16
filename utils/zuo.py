import hashlib
import pickle
import secrets
import math
import random
import os
from Crypto.Cipher import AES

def primitive_hash_h(msg, k):
  m= hashlib.sha256(k)
  m.update(msg)
  hash_msg = m.digest()
  return hash_msg

def pseudo_permutation_P(key, raw, iv):
  cipher = AES.new(key,AES.MODE_CBC,iv) #raw must be multiple of 16
  return cipher.encrypt(raw)

def pseudo_inverse_permutation_P(key, ctext,iv):
  cipher = AES.new(key,AES.MODE_CBC,iv)
  return cipher.decrypt(ctext)

def bxor(b1, b2):
  assert len(b1) == len(b2)
  result = bytearray(b1)
  for i, b in enumerate(b2):
    result[i] ^= b
  return bytes(result)

class Zuo(object):
  """docstring for zuo
  dbfile: string, the path of db file
  bslength: the lenght of bitmap
  """
  def __init__(self, dbfile, bslength):
    self.bslength = bslength
    with open(dbfile, 'rb') as f:
      self.db = pickle.load(f)
    self.keyword_list = [k for k in self.db.keys()]
    self.keyword_list.sort()
    self.tree_height = math.ceil(math.log(len(self.keyword_list), 2))

    self.K = os.urandom(16)
    self.iv = os.urandom(16)
    self.keyword2sk = {}

  def gen_edb(self):
    self.edb = {}
    self.localtree = {}

    expand_db = {}
    for i in range(self.tree_height, -1, -1): # 树节点的数量： 2 ** (height + 1) - 1
      for j in range(2 ** i):
        temp_keyword = bin(j)[2:].rjust(i + 1, "0")
        if i == self.tree_height:
          expand_db.setdefault(temp_keyword, self.db.get(self.keyword_list[j], set()))
          self.localtree.setdefault(temp_keyword, self.keyword_list[j])
        else:
          temp_fileid = expand_db.get(f"{temp_keyword}0") | expand_db.get(f"{temp_keyword}1")
          expand_db.setdefault(temp_keyword, temp_fileid)
          temp_val = self.localtree.get(temp_keyword + "0" + "1" * (self.tree_height - i - 1))
          self.localtree.setdefault(temp_keyword, temp_val)

    # 开始构建对应的 bitmap 与 edb    
    file_posi = {}
    file_list = list(expand_db.get("0"))
    for i, j in enumerate(file_list):
      file_posi.setdefault(j, i)
    for keyword in expand_db.keys():
      # 计算 keyword 的哈希
      hash_keyword = primitive_hash_h(keyword.encode("utf-8"), self.K)
      bs = self.__gen_bitmap(file_posi, expand_db.get(keyword))
      otp_key = secrets.token_bytes(int(self.bslength / 8))
      enc_bs = bxor(bs, otp_key)
      self.edb.setdefault(hash_keyword, enc_bs)
      self.keyword2sk.setdefault(hash_keyword, otp_key) # only for test, not used in real applications
    enc_file_list = [pseudo_permutation_P(self.K, fid.to_bytes(16, byteorder="big"), self.iv) for fid in file_list]
    self.edb.setdefault("file_index", enc_file_list)

    del self.keyword_list
    del self.db

  def gen_token(self, query_range):
    (left_node, right_node) = [self.__search_tree(x) for x in query_range]

    BRC_nodes = []
    i = self.tree_height + 1
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
    tokens_list = []
    for keyword in BRC_nodes:
      hash_keyword = primitive_hash_h(keyword.encode("utf-8"), self.K)
      tokens_list.append(hash_keyword)
    return tokens_list

  def search(self, token_list):
    search_result = []
    for token in token_list:
      search_result.append(self.edb.get(token))
    return search_result

  def gen_ids(self, search_result, tokens_list):
    # only for test
    final_result = set()
    for i, enc_bitmap in enumerate(search_result):
      otp_key = self.keyword2sk.get(tokens_list[i])
      bitmap = bxor(enc_bitmap, otp_key)
      temp_result = self.__parse_fileid(bitmap, self.edb.get("file_index"))
      final_result = final_result | temp_result
    return [pseudo_inverse_permutation_P(self.K, result, self.iv) for result in final_result]

  def __search_tree(self, query_value):
    keyword_node = "0"
    for i in range(0, self.tree_height):
      if query_value <= self.localtree.get(keyword_node):
        keyword_node += "0"
      else:
        keyword_node += "1"
    return keyword_node

  def __gen_bitmap(self, db_list, fileid_list):
    # bslength means the length of bitmap, that is the number of files.
    bs_list = ["0" for x in range(self.bslength)]
    for fileid in fileid_list:
      bs_list[db_list.get(fileid)] = "1"
    bs_string = ''.join(bs_list)
    return int(bs_string, 2).to_bytes(int(self.bslength / 8), byteorder="big")

  def __parse_fileid(self, bitmap, db_list):
    parse_id = set()
    bitmap_list = ''.join([bin(i)[2:].rjust(8, "0") for i in bitmap])
    for i, j in enumerate(bitmap_list):
      if i >= len(db_list):
        break
      if j == "1":
        parse_id.add(db_list[i])
    return parse_id 