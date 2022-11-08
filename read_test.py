import pickle

with open("./dataset/DB/db_512_80k", "rb") as f:
  db = pickle.load(f)

keyword_list = [k for k in db.keys()]
print(len(keyword_list))