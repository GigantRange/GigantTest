# 该程序用于验证 wang 的正确性
from utils.wang import Wang
from utils.trivial import Direct, gen_random_range

case_wang = Wang("./dataset/DB/db_512_80k")
case_trivia = Direct("./dataset/DB/db_512_80k")

case_wang.gen_edb()

for x in [10, 20, 50, 100, 500]:
	test_range = gen_random_range(case_trivia.keyword_list, x)
	query_range = [test_range[0], test_range[-1]]
	tokens = case_wang.gen_token(query_range)
	search_result = case_wang.search(tokens)
	verify_result = case_trivia.search(query_range)

	print(len(search_result) == len(verify_result))