import sympy as sp
from sympy import sqrt, integrate, symbols, simplify

# 정의
k = 8/3 - sqrt(6)
x = symbols('x', real=True)
t = symbols('t', real=True)

# f(x) = (1/3)(x-k)^3 + 2(x-k) + k
def f_func(val):
    return (val - k)**3/3 + 2*(val - k) + k

# k+1에서의 값
result = f_func(k + 1)
result_simplified = simplify(result)

# 5 - sqrt(6)과 비교
expected = 5 - sqrt(6)
expected_simplified = simplify(expected)

if abs(float(result_simplified - expected_simplified)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')