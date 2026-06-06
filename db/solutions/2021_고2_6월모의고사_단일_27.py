import sympy as sp
from sympy import symbols, log, solve, Eq

k = symbols('k', positive=True, real=True)
a = symbols('a', positive=True, real=True)

# 지수 관계식
eq1 = Eq(a**k, a**k)  # b = a^k
eq2 = Eq((a**k)**(2*k), a**(2*k**2))  # c = a^(2k^2)
eq3 = Eq((a**(2*k**2))**(3*k), a)  # c^(3k) = a

# 세 번째 식에서: a^(6k^3) = a^1
eq_main = Eq(6*k**3, 1)
sol_k3 = solve(eq_main, k**3)
k3_value = sol_k3[0]

# 검증
result = 120 * k3_value
if result == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')