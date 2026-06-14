from sympy import symbols, summation, solve

# 등차수열 정의: a_n = 14 - 2n
def a(n):
    return 14 - 2*n

def S(n):
    return sum(a(k) for k in range(1, n+1))

def T(n):
    return sum(abs(a(k)) for k in range(1, n+1))

# 조건 (가) 검증: S_7 = T_7
S7 = S(7)
T7 = T(7)
assert S7 == T7, f'S_7={S7}, T_7={T7} not equal'
assert S7 == 42, f'S_7={S7}, should be 42'

# 조건 (나) 검증: S_n + T_n = 84 for n >= 6
for n in range(6, 16):
    Sn = S(n)
    Tn = T(n)
    total = Sn + Tn
    assert total == 84, f'n={n}: S_n+T_n={total}, not 84'

# T_15 계산
result = T(15)
assert result == 114, f'T_15={result}, should be 114'

print('VERIFY_PASS')