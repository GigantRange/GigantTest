from utils.wang import Wang
from utils.zuo import Zuo
from utils.gigant import Gigant
from utils.trivial import gen_random_range, Direct
import pickle

keyword_number = 4096
test_file_number = [60, 100, 120]

for file_number in test_file_number:
  db_file = f"./dataset/DB/db_{keyword_number}_{file_number}k"

  """ TEST for gigant
  case_gigant = Gigant(db_file, 6264)
  case_gigant.gen_edb()
  with open(f"./dataset/EDB2/gigant/edb_{keyword_number}_{file_number}k", 'wb') as f:
    pickle.dump(case_gigant.edb, f)
  with open(f"./dataset/EDB2/gigant/local_{keyword_number}_{file_number}k", 'wb') as f:
    pickle.dump(case_gigant.localtree, f)
  """

  """ TEST for wang
  case_wang = Wang(db_file)
  case_wang.gen_edb()
  with open(f"./dataset/EDB2/wang/edb_{keyword_number}_{file_number}k", 'wb') as f:
    pickle.dump(case_wang.edb, f)
  with open(f"./dataset/EDB2/wang/local_{keyword_number}_{file_number}k", 'wb') as f:
    pickle.dump(case_wang.localtree, f)
  """

  case_zuo = Zuo(db_file, file_number * 1000)
  case_zuo.gen_edb()
  with open(f"./dataset/EDB2/zuo/edb_{keyword_number}_{file_number}k", 'wb') as f:
    pickle.dump(case_zuo.edb, f)
  with open(f"./dataset/EDB2/zuo/local_{keyword_number}_{file_number}k", 'wb') as f:
    pickle.dump(case_zuo.localtree, f)


  # case_zuo = Zuo(db_file, file_number * 1000)
  # case_wang = Wang(db_file)





