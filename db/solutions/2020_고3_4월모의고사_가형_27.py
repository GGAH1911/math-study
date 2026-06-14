import sympy as sp
from sympy import symbols, expand, limit, oo, solve, sqrt

CANDIDATE = 2

n = symbols('n', positive=True, integer=True)

# 원의 중심
a_n = n**2 + sp.Rational(1, 2)
b_n = 2*n - n**2 - sp.Rational(1, 2)

# 조건 1: 중심에서 접점으로의 벡터가 (1,1)에 수직
vec = (n - a_n, n - b_n)
perp_check = vec[0] + vec[1]  # (1,1)과의 내적
assert perp_check == 0, f"Perpendicularity check failed: {perp_check}"

# 조건 2: 원이 (1,0)과 (n,n)을 모두 지남
dist_1_0 = (1 - a_n)**2 + (0 - b_n)**2
dist_n_n = (n - a_n)**2 + (n - b_n)**2
dist_diff = expand(dist_1_0 - dist_n_n)
assert dist_diff == 0, f"Distance check failed: {dist_diff}"

# 극한 계산
a_n_minus_b_n = expand(a_n - b_n)
result = limit(a_n_minus_b_n / n**2, n, oo)

if result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: expected {CANDIDATE}, got {result}")