import sympy as sp
# (x^2+2/x)^6 의 x^6 계수?
CANDIDATE = 60
x = sp.symbols('x')
print('VERIFY_PASS' if sp.expand((x**2+2/x)**6).coeff(x, 6) == CANDIDATE else 'VERIFY_FAIL')
