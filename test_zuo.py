# 该程序用于验证 zuo 的正确性
from utils.zuo import Zuo
from utils.trivial import Direct, gen_random_range

case_zuo = Zuo("./dataset/DB/db_512_80k", 80000)
case_trivia = Direct("./dataset/DB/db_512_80k")

case_zuo.gen_edb()

for x in [10, 20, 50, 100, 500]:
	test_range = gen_random_range(case_trivia.keyword_list, x)
	query_range = [test_range[0], test_range[-1]]
	search_result = case_zuo.search(case_zuo.gen_token(query_range))
	final_result = case_zuo.gen_ids(search_result)
	verify_result = case_trivia.search(query_range)

	print(len(final_result) == len(verify_result))