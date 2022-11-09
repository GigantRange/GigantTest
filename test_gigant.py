from utils.gigant import Gigant

case_gigant = Gigant("./dataset/DB/db_512_80k", 1024)

case_gigant.gen_edb()

case_gigant.gen_localtree()