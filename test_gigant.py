from utils.gigant import Gigant

case_gigant = Gigant("./dataset/DB/db_512_80k", 1024)


case_gigant.gen_localtree()

case_gigant.gen_edb()

print(case_gigant.cluster_klist[0])



a = case_gigant.gen_token([-32.0087, 21.9566])

b = case_gigant.search(a)

# print(b)