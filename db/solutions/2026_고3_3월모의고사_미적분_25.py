import math

# 원 조건: sum_{k=1}^n a_k = sqrt(n+2)
# 따라서 a_n = sqrt(n+2) - sqrt(n+1) (n>=2), a_1 = sqrt(3)

def partial_sum(N):
    s = 0.0
    for k in range(1, N+1):
        if k == 1:
            ak = math.sqrt(3)
        else:
            ak = math.sqrt(k+2) - math.sqrt(k+1)
        s += ak
    return s

# 조건 자체 검증: 부분합이 sqrt(n+2)와 일치하는지
ok_cond = all(abs(partial_sum(N) - math.sqrt(N+2)) < 1e-9 for N in [1,2,5,10,50,100])

# 극한 검증: sqrt(n)*a_n -> 1/2 인지
guess = 1/2
vals = []
for N in [10**3, 10**4, 10**5, 10**6, 10**7]:
    aN = math.sqrt(N+2) - math.sqrt(N+1)
    vals.append(math.sqrt(N) * aN)

ok_limit = abs(vals[-1] - guess) < 1e-3 and abs(vals[-1] - guess) < abs(vals[0] - guess)

print('VERIFY_PASS' if (ok_cond and ok_limit) else 'VERIFY_FAIL')
