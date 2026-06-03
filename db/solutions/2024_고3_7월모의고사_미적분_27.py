import sympy as sp
from sympy import symbols, ln, integrate, simplify

t = symbols('t', real=True, positive=True)
f_t = 2*t*ln(t+1)

# 정적분 계산
result = integrate(f_t, (t, 1, 3))
result_simplified = simplify(result)

# 16ln(2) - 2와 비교
expected = 16*ln(2) - 2
expected_simplified = simplify(expected)

if simplify(result_simplified - expected_simplified) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')