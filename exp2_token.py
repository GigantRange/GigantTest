# 测试生成 tokens 的个数
# 数据集： db_4096_80k 
# 自变量： Range Size 的大小

from utils.wang import Wang
from utils.zuo import Zuo
from utils.gigant import Gigant
from utils.trivial import gen_random_range, Direct
import pandas as pd

keyword_number = 8192
mark_range = list(range(128, 8193, 32))
db_file = f"./dataset/DB/db_{keyword_number}_80k"

case_gigant = Gigant(db_file, 2048)
case_gigant.gen_edb()

case_wang = Wang(db_file)
case_wang.gen_edb()
# del case_wang.edb
case_zuo = Zuo(db_file, 80000)
case_zuo.gen_edb()

case_trivia = Direct(db_file)

tokens_result = {"gigant": [], "wang": [], "zuo": []}

def test_tokens(epoch, range_size):
  sum_tokens_list = [[], [], []]
  for i in range(epoch):
    test_range = gen_random_range(case_trivia.keyword_list, range_size)
    query_range = [test_range[0], test_range[-1]]
    tokens_list = [len(x.gen_token(query_range)) for x in [case_gigant, case_wang, case_zuo]]
    for x in range(0, 3):
      sum_tokens_list[x].append(tokens_list[x])
  return [sum(x) / epoch for x in sum_tokens_list]

for i in mark_range:
  [t1, t2, t3] = test_tokens(10000, i)
  tokens_result["gigant"].append(t1)
  tokens_result["wang"].append(t2)
  tokens_result["zuo"].append(t3)

data_frame = pd.DataFrame({
  "Range Size": mark_range,
  "Our Proposed Scheme": tokens_result["gigant"],
  "Range SSE-II": tokens_result["wang"],
  "FBDSSE-RQ": tokens_result["zuo"]
  })

data_frame.to_csv(f"./results/TEST2_TOKENS_{keyword_number}_80k.csv", index=False)