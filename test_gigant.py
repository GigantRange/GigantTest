from utils.gigant import Gigant
from utils.trivial import Direct, gen_random_range


case_gigant = Gigant("./dataset/DB/db_512_80k", 1024)
case_trivia = Direct("./dataset/DB/db_512_80k")

case_gigant.gen_edb()

# print(case_gigant.cluster_klist[0])
# print(type(case_gigant.edb.get(-38.1737)))

test_range = gen_random_range(case_trivia.keyword_list, 10)
# print(test_range)
query_range = [test_range[0], test_range[-1]]
tokens = case_gigant.gen_token(query_range)
search_result = case_gigant.search(tokens)
final_result = case_gigant.local_search(search_result)
print(len(final_result))

"""
# query_range = [test_range[0], test_range[-1]]

# query_range = [30.3222, 34.0558]

# a = case_gigant.gen_token([-32.0087, 21.9566])
tokens = case_gigant.gen_token(query_range)
search_result = case_gigant.search(tokens)
# print(case_gigant.local_position)

final_result = case_gigant.local_search(search_result)
print(len(final_result))

# d = case_trivia.search([-32.0087, 21.9566])
verify_result = case_trivia.search(query_range)
print(len(verify_result))

"""