# 주어진 조건을 만족하는지 검증
a10 = 113
sum_9 = a10 - 101  # 조건 2에서 도출

# 조건 1: sum(a_k, k=1..10) + sum(a_k, k=1..9) = 137
sum_10 = sum_9 + a10
cond1 = sum_10 + sum_9

# 조건 2: sum(a_k, k=1..10) - 2*sum(a_k, k=1..9) = 101
cond2 = sum_10 - 2*sum_9

if cond1 == 137 and cond2 == 101:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')