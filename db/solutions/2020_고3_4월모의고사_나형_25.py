CANDIDATE = 27
from sympy import symbols, integrate, Rational
x = symbols('x')
f_prime = 4*x**3 + 4*x + 1
F = integrate(f_prime, x)
# f(0) = 1 조건으로 C 결정
C = 1 - F.subs(x, 0)
f = F + C
result = f.subs(x, 2)
if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')