# 测试分组容量对 tokens 数量的影响

from utils.gigant import Gigant
from utils.trivial import gen_random_range, Direct

case_trivia = Direct("./dataset/DB/db_8192_80k")

case_gigant = Gigant("./dataset/DB/db_8192_80k", 568)
case_gigant.gen_edb()

tokens_list = []

for epoch in range(10000):
  test_range = gen_random_range(case_trivia.keyword_list, 1000)
  query_range = [test_range[0], test_range[-1]]

  tokens = case_gigant.gen_token(query_range)

  tokens_list.append(len(tokens))

print(sum(tokens_list) / 10000)

# print(len(tokens))



