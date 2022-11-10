import hashlib
import pickle
import secrets
import math
import random
import os
from Crypto.Cipher import AES

class Gigant(object):
  """docstring for Gigant"""
  def __init__(self, dbfile, bslength):
    self.bslength = bslength
    with open(dbfile, 'rb') as f:
      self.db = pickle.load(f)
    self.keyword_list = [k for k in self.db.keys()]
    self.keyword_list.sort()

  def gen_edb(self):
    # gen_edb 包含构建本地二叉树和加密索引两个步骤
    self.localtree = {}
    # self.cluster = {"flist": [], "klist": []}
    self.cluster_flist = []
    # 存储 cluster 中的文件 id
    self.cluster_klist = []
    # 存储 cluster 中的关键词内容
    self.edb = {}

    temp_group = []
    temp_value = []

    for i, keyword in enumerate(self.keyword_list):
      if len(temp_group) + len(self.db[keyword]) < self.bslength:
        temp_group.extend(self.db[keyword])
        temp_value.append(keyword)
        bit_string = "1" * len(temp_group) + "0" * int(self.bslength - len(temp_group))
        bs = self.__bs2bitmap(bit_string, self.bslength)
        self.edb.setdefault(keyword, bs)

        if i == len(self.keyword_list) - 1:
          self.cluster_flist.append(temp_group.copy())
          self.cluster_klist.append(temp_value.copy())
      else:
        self.cluster_flist.append(temp_group.copy())
        self.cluster_klist.append(temp_value.copy())
        temp_group = [*self.db[keyword]]
        temp_value = [keyword]
        bit_string = "1" * len(temp_group) + "0" * int(self.bslength - len(temp_group))
        bs = self.__bs2bitmap(bit_string, self.bslength)
        self.edb.setdefault(keyword, bs)

    self.cluster_height = math.ceil(math.log(len(self.cluster_flist), 2))
    # gen_list = [ [x[0], x[-1]] for x in self.cluster_klist]
    # padding_list = [ gen_list[-1] for x in range(2 ** self.cluster_height - len(gen_list))]
    gen_list = [ x[-1] for x in self.cluster_klist]
    padding_list = [ gen_list[-1] for x in range(2 ** self.cluster_height - len(gen_list))]
    # 此处的 padding_list 也是多余的存储，是否可以去掉？
    gen_list = gen_list + padding_list

    for i in range(self.cluster_height, -1, -1):
      for j in range(2 ** i):
        temp_keyword = bin(j)[2:].rjust(i + 1, "0")
        if i == self.cluster_height:
          self.localtree.setdefault(temp_keyword, gen_list[j])
        else:
          temp_val = self.localtree.get(temp_keyword + "0" + "1" * (self.cluster_height - i - 1))
          self.localtree.setdefault(temp_keyword, temp_val)

  def gen_token(self, query_range):
    self.flags = []
    self.local_position = [self.__search_tree(query_range[0]), self.__search_tree(query_range[1])]
    self.server_tokens = []

    local_cluster = self.cluster_klist[self.local_position[0]: self.local_position[1] + 1]
    # token1 = searchby2(left_cluster, query_range[0], "0")
    # token2 = searchby2(left_cluster, query_range[0], "1")
    if query_range[0] == local_cluster[0][0] and query_range[1] == local_cluster[-1][-1]:
      # 不需要搜索
      return self.server_tokens
    else:
      if query_range[0] != local_cluster[0][0]:
        temp_token = local_cluster[0][local_cluster[0].index(query_range[0]) - 1]
        # 此处可以优化，使用二分查找替代 index
        self.server_tokens.append(temp_token)
        self.flags.append("l")
      if query_range[1] != local_cluster[-1][-1]:
        self.server_tokens.append(query_range[1])
        self.flags.append("r")
    return self.server_tokens

  def search(self, token_list):
    search_result = []
    for token in token_list:
      search_result.append(self.edb.get(token))
    return search_result

  def local_search(self, search_result):
    last_bitmap = self.__bs2bitmap("1" * (self.bslength), self.bslength)
    final_result = []
    (p1, p2) = self.local_position
    # print(self.local_position)
    if len(search_result) == 0:
      for file_list in self.cluster_flist[p1 : p2 + 1]:
        final_result.extend(file_list)
      return final_result
    elif len(search_result) == 2:
      if p1 == p2:
        comp_bitmap = bytearray()
        for x, y in zip(search_result[0], search_result[1]):
          comp_bitmap.append(x ^ y)
        final_result.extend(self.__parse_fileid(comp_bitmap[0 : len(self.cluster_flist[p1])], self.cluster_flist[p1]))
      else:
        left_bitmap = bytearray()
        for x, y in zip(search_result[0], last_bitmap):
          left_bitmap.append(x ^ y)
        final_result.extend(self.__parse_fileid(left_bitmap, self.cluster_flist[p1]))
        right_bitmap = search_result[-1]
        final_result.extend(self.__parse_fileid(right_bitmap, self.cluster_flist[p2]))
        for file_list in self.cluster_flist[p1 + 1 : p2]:
          final_result.extend(file_list)
        # final_result.extend(self.cluster_flist[p1 + 1 : p2])
    else:
      if "l" in self.flags:
        left_bitmap = bytearray()
        for x, y in zip(search_result[0], last_bitmap):
          left_bitmap.append(x ^ y)        
        final_result.extend(self.__parse_fileid(left_bitmap[0: len(self.cluster_flist[p1])], self.cluster_flist[p1]))
        for file_list in self.cluster_flist[p1 + 1 : p2 + 1]:
          final_result.extend(file_list)
        # final_result.extend(self.cluster_flist[p1 + 1 : p2 + 1])
      if "r" in self.flags:
        right_bitmap = search_result[-1]
        final_result.extend(self.__parse_fileid(right_bitmap[0: len(self.cluster_flist[p2])], self.cluster_flist[p2]))
        for file_list in self.cluster_flist[p1 : p2]:
          final_result.extend(file_list)
        # final_result.extend(self.cluster_flist[p1: p2])
    return final_result

  def __search_tree(self, query_value):
    keyword_node = "0"
    for i in range(0, self.cluster_height):
      # if query_value > self.localtree.get(keyword_node)[-1]:
      if query_value > self.localtree.get(keyword_node):
        keyword_node += "1"
      else:
        keyword_node += "0"
      keyword_posi = int(keyword_node, 2)
    # 对 query_range 的左右进行判断，找到对应的 group
    # return self.cluster_klist[keyword_posi]
    return keyword_posi

  def __bs2bitmap(self, bit_string, bslength):
    # bslength 是 bits 的个数，因此在转换成 bytes 时需要除以 8
    # 输入的是 bit string，转换后的为一个 bitmap，数据类型为 bytes
    return int(bit_string, 2).to_bytes(int(bslength / 8), byteorder="big")

  def __parse_fileid(self, bitmap, db_list):
    parse_id = []
    bitmap_list = ''.join([bin(i)[2:].rjust(8, "0") for i in bitmap])
    for i, j in enumerate(bitmap_list):
      if i >= len(db_list):
        break
      if j == "1":
        parse_id.append(db_list[i])
    return parse_id