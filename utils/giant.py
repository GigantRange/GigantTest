import hashlib
import pickle
import secrets
import math
import random
import os
from Crypto.Cipher import AES

class Giant(object):
  """docstring for Gigant"""
  def __init__(self, dbfile, bslength):
    self.bslength = bslength
    with open(dbfile, 'rb') as f:
      self.db = pickle.load(f)
    self.keyword_list = [k for k in self.db.keys()]
    self.keyword_list.sort()

  def gen_edb(self):
    pass

  def gen_localtree(self):
    pass

  def gen_token(self):
    pass

  def search(self):
    pass
