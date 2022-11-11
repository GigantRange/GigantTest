# 测试生成 tokens 的个数
# 数据集： db_4096_80k 
# 自变量： Range Size 的大小

from utils.wang import Wang
from utils.zuo import Zuo
from utils.gigant import Gigant
from utils.trivial import gen_random_range, Direct

case_gigant = Gigant("./dataset/DB/db_4096_80k", 2048)
case_gigant.gen_edb()

case_trivia = Direct("./dataset/DB/db_4096_80k")

test_range = gen_random_range(case_trivia.keyword_list, 200)
# print(test_range)
query_range = [test_range[0], test_range[-1]]
tokens = case_gigant.gen_token(query_range)
print(len(tokens))
search_result = case_gigant.search(tokens)
final_result = case_gigant.local_search(search_result)
print(len(final_result))

verify_result = case_trivia.search(query_range)
print(len(verify_result))

# 记录哪些值？

# Range Size，tokens 数量（平均）-1，2，3