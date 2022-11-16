# 该程序用于验证 gigant 的正确性
from utils.gigant import Gigant
from utils.trivial import Direct, gen_random_range

case_gigant = Gigant("./dataset/DB/db_512_80k", 1600)
case_trivia = Direct("./dataset/DB/db_512_80k")

case_gigant.gen_edb()

for x in [10, 20, 50, 100, 500]:
	test_range = gen_random_range(case_trivia.keyword_list, x)
	query_range = [test_range[0], test_range[-1]]
	tokens = case_gigant.gen_token(query_range)
	search_result = case_gigant.search(tokens)
	final_result = case_gigant.local_search(search_result, tokens)
	verify_result = case_trivia.search(query_range)
	print(len(final_result) == len(verify_result))