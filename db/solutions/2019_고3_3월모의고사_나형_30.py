from sympy import symbols, expand, limit, oo, simplify

CANDIDATE = 4

n = symbols('n', positive=True, integer=True)

# S_n 공식
S_n = (4*n**3 + 3*n**2 - 4*n) / 3

# S_{n+1} 공식
S_n_plus_1 = (4*(n+1)**3 + 3*(n+1)**2 - 4*(n+1)) / 3
S_n_plus_1_expanded = simplify(S_n_plus_1)

# 차이 계산
difference = simplify(S_n_plus_1_expanded - S_n)

# 극한 계산
limit_value = limit(difference / n**2, n, oo)

if limit_value == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected {CANDIDATE}, got {limit_value}')