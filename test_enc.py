import hashlib
import pickle
import secrets
import math
import random
import os
from Crypto.Cipher import AES

from utils.trivial import Direct

case_trivia = Direct("./dataset/DB/db_4096_80k")

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

test_id = 2948650
k = os.urandom(16)
iv = os.urandom(16)

for keyword in case_trivia.keyword_list:
  hash_keyword = primitive_hash_h(str(keyword).encode("utf-8"), k)


enc_id = pseudo_permutation_P(k, test_id.to_bytes(16, byteorder="big"), iv)
print(enc_id)

dec_id = pseudo_inverse_permutation_P(k, enc_id, iv)
print(dec_id)
print(int.from_bytes(dec_id, byteorder="big"))

# print(case_trivia.db.get(case_trivia.keyword_list[10]))

# message = int(-14).to_bytes(8, byteorder="big", signed=True)
# .encode("utf-8")
# enc_content = primitive_hash_h(message)
# print(enc_content)

