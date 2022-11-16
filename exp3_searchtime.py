# 测试搜索 EDB 的时间
# 数据集：db_4096_80k
# 自变量：Range Size

import time
import pandas as pd
from decimal import Decimal
from utils.wang import Wang
from utils.zuo import Zuo
from utils.gigant import Gigant
from utils.trivial import gen_random_range, Direct

epoch = 100
db_file = "./dataset/DB/db_4096_80k"

search_time = {"gigant": [], "wang": [], "zuo": []}

case_trivia = Direct(db_file)
case_gigant = Gigant(db_file, 6264)
case_gigant.gen_edb()
case_zuo = Zuo(db_file, 80000)
case_zuo.gen_edb()
case_wang = Wang(db_file)
case_wang.gen_edb()

test_range_size = list(range(500, 4001, 500))

def test_search_time(obj, epoch, search_ranges, flag=0):
	start = time.process_time()
	for i in range(epoch):
		search_tokens = obj.gen_token(search_ranges[i])
		search_result = obj.search(search_tokens)
		if flag == 1:
			obj.local_search(search_result, search_tokens)
		if flag == 2:
			obj.gen_ids(search_result, search_tokens)

	end = time.process_time()
	cost = Decimal((Decimal(end) - Decimal(start)) * 1000 / epoch).quantize(Decimal("0.00"))
	return cost

for range_size in test_range_size:
	search_ranges = [gen_random_range(case_trivia.keyword_list, range_size) for x in range(epoch)]

	search_time["gigant"].append(test_search_time(case_gigant, epoch, search_ranges, 1))
	search_time["wang"].append(test_search_time(case_wang, epoch, search_ranges))
	search_time["zuo"].append(test_search_time(case_zuo, epoch, search_ranges, 2))

data_frame = pd.DataFrame({
	"Range Size": test_range_size,
	"Our Proposed Scheme": search_time["gigant"],
	"Range SSE-II": search_time["wang"],
	"FBDSSE-RQ": search_time["zuo"]
	})

data_frame.to_csv("./results/TEST3_SEARCH_4096_80k.csv", index=False)