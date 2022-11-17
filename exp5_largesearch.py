from utils.gigant import Gigant
from utils.trivial import gen_random_range, Direct
import pickle
import time
from decimal import Decimal


case_trivia = Direct("./dataset/DB/db_65536_1000k")
case_gigant = Gigant("./dataset/DB/db_65536_1000k", 6264)
case_gigant.gen_edb()
epoch = 1000

test_range_size = list(range(5000, 60001, 5000))

with open("./dataset/EDB2/gigant/edb_65536_1000k", 'wb') as f:
  pickle.dump(case_gigant.edb, f)

with open("./dataset/EDB2/gigant/local_65536_1000k", 'wb') as f:
  pickle.dump(case_gigant.localtree, f)

def test_search_time(obj, epoch, search_ranges):
  start = time.process_time()
  for i in range(epoch):
    search_tokens = obj.gen_token(search_ranges[i])
    search_result = obj.search(search_tokens)
    obj.local_search(search_result, search_tokens)
  end = time.process_time()
  cost = Decimal((Decimal(end) - Decimal(start)) * 1000 / epoch).quantize(Decimal("0.00"))
  return cost

for range_size in test_range_size:
  search_ranges = [gen_random_range(case_trivia.keyword_list, range_size) for x in range(epoch)]
  test_time = test_search_time(case_gigant, epoch, search_ranges)
  print(f"{range_size}:{test_time}")

"""
epoch = 10
start = time.process_time()
for i in range(epoch):
  case_gigant.gen_edb()
end = time.process_time()
cost = Decimal((Decimal(end) - Decimal(start)) * 1000 / epoch).quantize(Decimal("0.00"))
print(cost)
"""













