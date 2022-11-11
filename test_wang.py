from utils.wang import Wang
from utils.trivial import Direct, gen_random_range

case_wang = Wang("./dataset/DB/db_512_80k")
case_trivia = Direct("./dataset/DB/db_512_80k")

case_wang.gen_edb()

# print(case_wang.localtree.get("0"))

test_range = gen_random_range(case_trivia.keyword_list, 200)
query_range = [test_range[0], test_range[-1]]
print(query_range)

print(case_wang.gen_token(query_range))

# print(case_wang.gen_token(query_range))

