from utils.zuo import Zuo
from utils.trivial import Direct, gen_random_range

case_zuo = Zuo("./dataset/DB/db_512_80k", 80000)
case_trivia = Direct("./dataset/DB/db_512_80k")

# print(case_zuo.tree_height)
# 本地二叉树高度为 10，需要记录 2^11 - 1 个节点

# print(case_zuo.keyword_list)

case_zuo.gen_edb()

# print(len(case_zuo.expand_db.get("0")))

# print(case_zuo.keyword_list[0])
# query_range = [case_zuo.keyword_list[0], case_zuo.keyword_list[1]]
# search_tokens = case_zuo.gen_token(query_range)
# print(search_tokens)
# search_result1 = [case_zuo.edb.get("0000000000")]
# final_result1 = case_zuo.get_ids(search_result1)
# print(len(final_result1))

# print(case_zuo.db.get(-38.1737))
# print(len(case_zuo.db.get(-37.6689)))

# query_range = [case_zuo.keyword_list[0], case_zuo.keyword_list[1]]
test_range = gen_random_range(case_trivia.keyword_list, 200)
query_range = [test_range[0], test_range[-1]]
print(query_range)

search_result = case_zuo.search(case_zuo.gen_token(query_range))

final_result = case_zuo.gen_ids(search_result)

print(len(final_result))

verify_result = case_trivia.search(query_range)
print(len(verify_result))

# print(len(case_zuo.expand_db.keys()))

