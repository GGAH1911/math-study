import sympy as sp
from sympy import symbols, Abs, diff, solve

x = symbols('x')
a, b, c = -sp.Rational(1, 6), 2, -3

def f(x_val):
    return a*x_val**3 + b*x_val**2 + c*x_val

def g(x_val):
    return c*x_val

def h(x_val):
    return abs(f(x_val)) + g(x_val)

# 검증
k = 6
h_k = h(k)
h_3 = h(3)
h_6 = h(6)
h_11 = h(11)
result = k * (h_6 - h_11)

print(f'h({k}) = {h_k}')
print(f'h(3) = {h_3}')
print(f'h(6) = {h_6}')
print(f'h(11) = {h_11}')
print(f'k × {{h(6) - h(11)}} = {result}')

if h_k == 0 and h_3 == -sp.Rational(9, 2) and result == 121:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')