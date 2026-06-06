from sympy import symbols, solve, summation

a1, m = symbols('a1 m', integer=True, positive=True)

# 등차수열: a_n = a1 + 2(n-1)
def a(n):
    return a1 + 2*(n-1)

# 조건 1: sum(a_{k+1} for k=1 to m) = 240
cond1 = sum(a(k+1) for k in range(1, 13)) - 240  # m=12 대입

# 조건 2: sum(a_k + m for k=1 to m) = 360
cond2 = sum(a(k) + 12 for k in range(1, 13)) - 360  # m=12 대입

# a1 풀이
a1_val = 7  # 위에서 계산한 값

# a_m = a_12 계산
a_m = a1_val + 2*(12-1)

# 검증
sum1 = sum(a1_val + 2*k for k in range(1, 13))
sum2 = sum((a1_val + 2*(k-1)) + 12 for k in range(1, 13))

if sum1 == 240 and sum2 == 360 and a_m == 29:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')