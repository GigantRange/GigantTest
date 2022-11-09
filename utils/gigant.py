import hashlib
import pickle
import secrets
import math
import random
import os
from Crypto.Cipher import AES

def list2binary(bit_string, bslength):
  return int(bit_string, 2).to_bytes(int(bslength / 8), byteorder="big")

class Gigant(object):
  """docstring for Gigant"""
  def __init__(self, dbfile, bslength):
    self.bslength = bslength
    with open(dbfile, 'rb') as f:
      self.db = pickle.load(f)
    self.keyword_list = [k for k in self.db.keys()]
    self.keyword_list.sort()

  def gen_localtree(self):
    self.localtree = {}
    self.cluster_flist = []
    # 存储 cluster 中的文件 id
    self.cluster_klist = []
    # 存储 cluster 中的关键词内容
    self.bsdb = {}

    temp_group = []
    temp_value = []

    for i, keyword in enumerate(self.keyword_list):
      if len(temp_group) + len(self.db[keyword]) < self.bslength:
        temp_group.extend(self.db[keyword])
        temp_value.append(keyword)
        bit_string = "1" * len(temp_group) + "0" * int(self.bslength - len(temp_group))
        bs = list2binary(bit_string, self.bslength)
        self.bsdb.setdefault(keyword, bs)

        if i == len(self.keyword_list) - 1:
          self.cluster_flist.append(temp_group.copy())
          self.cluster_klist.append(temp_value.copy())
      else:
        self.cluster_flist.append(temp_group.copy())
        self.cluster_klist.append(temp_value.copy())
        temp_group = [*self.db[keyword]]
        temp_value = [keyword]
        bit_string = "1" * len(temp_group) + "0" * int(self.bslength - len(temp_group))
        bs = list2binary(bit_string, self.bslength)
        self.bsdb.setdefault(keyword, bs)

    cluster_height = math.ceil(math.log(len(self.cluster_flist), 2))
    gen_list = [ [x[0], x[-1]] for x in self.cluster_klist]
    padding_list = [ gen_list[-1] for x in range(2 ** cluster_height - len(gen_list))]
    gen_list = gen_list + padding_list

    for i in range(cluster_height, -1, -1):
      for j in range(2 ** i):
        temp_keyword = bin(j)[2:].rjust(i + 1, "0")
        if i == cluster_height:
          self.localtree.setdefault(temp_keyword, gen_list[j])
        else:
          temp_val = self.localtree.get(temp_keyword + "0" + "1" * (cluster_height - i - 1))
          self.localtree.setdefault(temp_keyword, temp_val)

  def gen_edb(self):
    self.edb = {}

  def gen_token(self):
    pass

  def search(self):
    pass