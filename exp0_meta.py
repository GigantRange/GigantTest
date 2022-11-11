# 测试各个方案 tokens 的数量
import pickle
import pandas as pd
from utils.wang import Wang
from utils.zuo import Zuo
from utils.gigant import Gigant
from utils.trivial import gen_random_range

# case_wang = Wang("./dataset/DB/db_4096_80k")
# case_wang.gen_edb()
# with open("./dataset/EDB2/wang/local_4096_80k", "wb") as f:
#   pickle.dump(case_wang.localtree, f)
# with open("./dataset/EDB2/wang/edb_4096_80k", "wb") as f:
#   pickle.dump(case_wang.edb, f)

# case_zuo = Zuo("./dataset/DB/db_4096_80k", 80000)
# case_zuo.gen_edb()
# with open("./dataset/EDB2/zuo/local_4096_80k", "wb") as f:
#   pickle.dump(case_zuo.localtree, f)
# with open("./dataset/EDB2/zuo/edb_4096_80k", "wb") as f:
#   pickle.dump(case_zuo.edb, f)

# case_gigant = Gigant("./dataset/DB/db_4096_80k", 2048)
# case_gigant.gen_edb()
# with open("./dataset/EDB2/gigant/local_4096_80k", "wb") as f:
#   pickle.dump(case_gigant.localtree, f)
# with open("./dataset/EDB2/gigant/edb_4096_80k", "wb") as f:
#   pickle.dump(case_gigant.edb, f)

db_list = ["./dataset/DB/db_512_80k", 
           "./dataset/DB/db_1024_80k",
           "./dataset/DB/db_2048_80k", 
           "./dataset/DB/db_4096_40k",
           "./dataset/DB/db_4096_60k",
           "./dataset/DB/db_4096_80k",
           "./dataset/DB/db_4096_100k",
           "./dataset/DB/db_4096_120k",
           "./dataset/DB/db_8192_80k",
           "./dataset/DB/db_65536_1000k"
           ]

def de_meta(file_name, n, d, k, range_bound, max_klength):
  with open(file_name, 'rb') as f:
    db = pickle.load(f)
  keyword_list = [k for k in db.keys()]
  keyword_list.sort()

  keyword_length = [len(db.get(k)) for k in keyword_list]

  n.append(file_name.split("/")[-1])
  d.append(sum(keyword_length)) # 文件数
  k.append(len(keyword_list)) # 关键词数
  range_bound.append([keyword_list[0], keyword_list[-1]])
  max_klength.append(max(keyword_length))
  # return (d, k, range_bound, max_klength)

# x = de_meta(db_list[0])
# print(x)

n = []
d = []
k = []
range_bound = []
max_klength = []

for db_file in db_list:
  db_info = de_meta(db_file, n, d, k, range_bound, max_klength)


data_frame = pd.DataFrame({
  "File Name": n, 
  "# of Documents": d, 
  "# of Keywords": k,
  "Range Bound": range_bound,
  "Max # of Docuemnts for a Keyword": max_klength
  })

data_frame.to_csv("./results/DB_INFO.csv", index=False)
