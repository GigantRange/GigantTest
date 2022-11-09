from utils.wang import Wang

case_wang = Wang("./dataset/DB/db_512_80k")

case_wang.gen_edb()
case_wang.gen_localtree()

# print(case_wang.localtree.get("0"))

query_range = [case_wang.keyword_list[2], case_wang.keyword_list[251]]

print(case_wang.gen_token(query_range))

# print(case_wang.gen_token(query_range))

