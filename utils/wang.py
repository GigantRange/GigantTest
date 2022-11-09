import hashlib
import pickle
import secrets
import math
import random
import os
from Crypto.Cipher import AES

class Wang(object):
  """docstring for Wang"""
  def __init__(self, dbfile):
    with open(dbfile, 'rb') as f:
      self.db = pickle.load(f)
    self.keyword_list = [k for k in self.db.keys()]
    self.keyword_list.sort()
    self.tree_height = math.ceil(math.log(len(self.keyword_list), 2))

  def gen_edb(self):
    self.edb = {}
    self.edb.setdefault("none", set())
    for i, keyword in enumerate(self.keyword_list):
      self.edb.setdefault(keyword, self.db.get(keyword))
      if i != 0: self.edb[keyword] = self.edb[keyword].union(self.edb.get(self.keyword_list[i-1]))

  def gen_localtree(self):
    # 根据关键词数量，决定树的高度
    self.localtree = {}
    for i in range(self.tree_height, -1, -1):
      for j in range(2 ** i):
        temp_keyword = bin(j)[2:].rjust(i + 1, "0")
        if i == self.tree_height:
          self.localtree.setdefault(temp_keyword, self.keyword_list[j])
        else:
          temp_val = self.localtree.get(temp_keyword + "0" + "1" * (self.tree_height - i - 1))
          self.localtree.setdefault(temp_keyword, temp_val)

  def gen_token(self, query_range):
    token1 = self.__search_tree(query_range[0], "0")
    token2 = self.__search_tree(query_range[1], "1")
    return (token1, token2)

  def __search_tree(self, query_value, flag):
    # flag == 0: is left bound
    # flag == 1: is right bound
    keyword_node = "0"
    for i in range(0, self.tree_height):
      if query_value <= self.localtree.get(keyword_node):
        keyword_node += "0"
      else:
        keyword_node += "1"
      keyword_posi = int(keyword_node, 2)
    if flag == "0":
      if keyword_posi == 0:
        return "none"
      return self.keyword_list[keyword_posi - 1]
      # return int(keyword_node, 2) - 1
    return self.keyword_list[keyword_posi]

  def search(self, token_list):
    (token1, token2) = token_list
    result_2 = self.edb.get(token2)
    result_1 = self.edb.get(token1)
    # 少一个解密的过程
    search_result = result_2 - result_1
    return search_result