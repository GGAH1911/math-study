# 조건을 만족하는 구체적 수열로 검증
a = [22, 7, 0, 0, 0, 0, 0, 0, 0, 0]

# 조건 1: sum_{k=1}^{10} k*a_k = 36
cond1 = sum((k+1) * a[k] for k in range(10))

# 조건 2: sum_{k=1}^{9} k*a_{k+1} = 7
cond2 = sum((k+1) * a[k+1] for k in range(9))

# 구하는 값: sum_{k=1}^{10} a_k
answer = sum(a)

if cond1 == 36 and cond2 == 7 and answer == 29:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')