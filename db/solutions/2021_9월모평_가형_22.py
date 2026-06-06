from math import comb
from sympy import symbols, expand

CANDIDATE = 24

# 이항정리: (x + 4/x^2)^6 = sum_{k=0}^{6} C(6,k) * x^(6-k) * (4/x^2)^k
#                           = sum_{k=0}^{6} C(6,k) * 4^k * x^(6-3k)
# x^3 항의 조건: 6-3k = 3 => k = 1
# 계수 = C(6,1) * 4^1 = 6 * 4 = 24

# 방법 1: 이항정리 직접 계산
k = 1
coeff_direct = comb(6, k) * (4**k)

# 방법 2: sympy 전개로 검증
x = symbols('x')
expr = (x + 4/x**2)**6
expanded = expand(expr)
coeff_sympy = expanded.coeff(x, 3)

# CANDIDATE 검증 (원래 식으로부터 계산된 값과 비교)
if coeff_direct == CANDIDATE and coeff_sympy == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")