from utils.zuo import Zuo

case_zuo = Zuo("./dataset/DB/db_512_80k", 80000)

print(case_zuo.tree_height)
# 本地二叉树高度为 10，需要记录 2^11 - 1 个节点

# print(case_zuo.keyword_list)

case_zuo.gen_edb()

# print(len(case_zuo.expand_db.get("0")))

# print(case_zuo.edb.get("0"))

query_range = [case_zuo.keyword_list[0], case_zuo.keyword_list[4]]
case_zuo.search(query_range)



# print(len(case_zuo.expand_db.keys()))