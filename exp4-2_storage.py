from utils.wang import Wang
from utils.zuo import Zuo
from utils.gigant import Gigant
from utils.trivial import gen_random_range, Direct
import pickle

test_keyword_number = [2048, 4096, 8192]
file_number = 80

for keyword_number in test_keyword_number:
  db_file = f"./dataset/DB/db_{keyword_number}_{file_number}k"

  # """ TEST for gigant
  case_gigant = Gigant(db_file, 6264)
  case_gigant.gen_edb()
  with open(f"./dataset/EDB3/gigant/edb_{keyword_number}_{file_number}k", 'wb') as f:
    pickle.dump(case_gigant.edb, f)
  with open(f"./dataset/EDB3/gigant/local_{keyword_number}_{file_number}k", 'wb') as f:
    pickle.dump(case_gigant.localtree, f)
  # """

  """
  case_zuo = Zuo(db_file, file_number * 1000)
  case_zuo.gen_edb()
  with open(f"./dataset/EDB2/zuo/edb_{keyword_number}_{file_number}k", 'wb') as f:
    pickle.dump(case_zuo.edb, f)
  with open(f"./dataset/EDB2/zuo/local_{keyword_number}_{file_number}k", 'wb') as f:
    pickle.dump(case_zuo.localtree, f)
  """

  """
  case_wang = Wang(db_file)
  case_wang.gen_edb()
  with open(f"./dataset/EDB2/wang/edb_{keyword_number}_{file_number}k", 'wb') as f:
    pickle.dump(case_wang.edb, f)
  with open(f"./dataset/EDB2/wang/local_{keyword_number}_{file_number}k", 'wb') as f:
    pickle.dump(case_wang.localtree, f)
  """






