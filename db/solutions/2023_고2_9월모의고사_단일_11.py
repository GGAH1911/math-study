import sympy as sp
from sympy import sqrt, symbols, simplify

r = sqrt(2)
a1 = 3

# 검증: a_n = 3 * r^(n-1)
a3 = a1 * r**2
a5 = a1 * r**4
a7 = a1 * r**6

# S_n = a1(r^n - 1)/(r - 1)
S2 = a1 * (r**2 - 1) / (r - 1)
S4 = a1 * (r**4 - 1) / (r - 1)

# 주어진 조건 검증
lhs = S4 / S2
rhs = 6 * a3 / a5

lhs_simplified = simplify(lhs)
rhs_simplified = simplify(rhs)

if simplify(lhs_simplified - rhs_simplified) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')