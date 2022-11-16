# 测试生成 EDB 的时间，该时间包含构造本地二叉树
# 数据集：db_*_80k
# 自变量：关键词数量

import time
import pandas as pd
from decimal import Decimal
from utils.wang import Wang
from utils.zuo import Zuo
from utils.gigant import Gigant
from utils.trivial import gen_random_range, Direct

test_keyword_number = [512, 1024, 2048, 4096, 8192]
file_number = 80
epoch = 10

setup_time = {"gigant": [], "wang": [], "zuo": []}

def test_setup_time(obj, epoch):
	start = time.process_time()
	for i in range(epoch):
		obj.gen_edb()
	end = time.process_time()
	cost = Decimal((Decimal(end) - Decimal(start)) * 1000 / epoch).quantize(Decimal("0.00"))
	return cost

for keyword_number in test_keyword_number:
	db_file = f"./dataset/DB/db_{keyword_number}_{file_number}k"
	case_trivia = Direct(db_file)
	case_gigant = Gigant(db_file, 6264)
	case_zuo = Zuo(db_file, file_number * 1000)
	case_wang = Wang(db_file)

	# print(len(case_gigant.keyword_list))

	setup_time["gigant"].append(test_setup_time(case_gigant, epoch))
	setup_time["wang"].append(test_setup_time(case_wang, epoch))
	setup_time["zuo"].append(test_setup_time(case_zuo, epoch))

data_frame = pd.DataFrame({
	"Keyword Number": test_keyword_number,
	"Our Proposed Scheme": setup_time["gigant"],
	"Range SSE-II": setup_time["wang"],
	"FBDSSE-RQ": setup_time["zuo"]
	})

data_frame.to_csv(f"./results/TEST1_SETUP_{file_number}k.csv", index=False)