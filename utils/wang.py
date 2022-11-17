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

class Wang(object):
  """docstring for Wang"""
  def __init__(self, dbfile):
    with open(dbfile, 'rb') as f:
      self.db = pickle.load(f)
    self.keyword_list = [k for k in self.db.keys()]
    self.keyword_list.sort()
    self.tree_height = math.ceil(math.log(len(self.keyword_list), 2))

    self.K = os.urandom(16)
    self.iv = os.urandom(16)

  def gen_edb(self):
    self.edb = {}
    self.localtree = {}

    self.edb.setdefault(primitive_hash_h("none".encode("utf-8"), self.K), set())
    for i, keyword in enumerate(self.keyword_list):
      # 计算 keyword 的哈希
      hash_keyword = primitive_hash_h(str(keyword).encode("utf-8"), self.K)
      enc_file_list = [pseudo_permutation_P(self.K, fid.to_bytes(16, byteorder="big"), self.iv) for fid in self.db.get(keyword)]
      self.edb.setdefault(hash_keyword, set(enc_file_list))
      if i != 0: 
        self.edb[hash_keyword] = self.edb[hash_keyword].union(self.edb.get(primitive_hash_h(str(self.keyword_list[i-1]).encode("utf-8"), self.K)))

        # if i > 8000:
          # with open("./temp", 'wb') as f:
            # pickle.dump(self.edb[primitive_hash_h(str(self.keyword_list[i-1]).encode("utf-8"), self.K)], f)
          # del self.edb[primitive_hash_h(str(self.keyword_list[i-1]).encode("utf-8"), self.K)]

    # del self.edb
    # del self.db

    for i in range(self.tree_height, -1, -1):
      for j in range(2 ** i):
        temp_keyword = bin(j)[2:].rjust(i + 1, "0")
        if i == self.tree_height:
          self.localtree.setdefault(temp_keyword, self.keyword_list[j])
        else:
          temp_val = self.localtree.get(temp_keyword + "0" + "1" * (self.tree_height - i - 1))
          self.localtree.setdefault(temp_keyword, temp_val)

    # del self.db
    del self.keyword_list

  def gen_token(self, query_range):
    token1 = self.__search_tree(query_range[0], "0")
    token2 = self.__search_tree(query_range[1], "1")
    hash_token1 = primitive_hash_h(str(token1).encode("utf-8"), self.K)
    hash_token2 = primitive_hash_h(str(token2).encode("utf-8"), self.K)
    return (hash_token1, hash_token2)

  def search(self, token_list):
    (token1, token2) = token_list
    result_2 = self.edb.get(token2)
    result_1 = self.edb.get(token1)
    enc_search_result = result_2 - result_1
    search_result = [pseudo_inverse_permutation_P(self.K, result, self.iv) for result in enc_search_result]
    return search_result

  def __search_tree(self, query_value, flag):
    # flag == 0: is left bound
    # flag == 1: is right bound
    keyword_node = "0"
    for i in range(0, self.tree_height):
      if query_value <= self.localtree.get(keyword_node):
        keyword_node += "0"
      else:
        keyword_node += "1"
    if flag == "0":
      keyword_posi = int(keyword_node, 2)
      if keyword_posi == 0:
        return "none"
      lleft_keyword = bin(keyword_posi - 1)[2:].rjust(self.tree_height + 1, "0")
      return self.localtree.get(lleft_keyword)
    return self.localtree.get(keyword_node)