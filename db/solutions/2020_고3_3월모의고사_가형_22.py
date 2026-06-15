import sympy as sp
# f(x)=(2x+3)(x^2+5), f'(1)?
CANDIDATE = 22
x = sp.symbols('x')
f = (2*x + 3)*(x**2 + 5)
print('VERIFY_PASS' if sp.diff(f, x).subs(x, 1) == CANDIDATE else 'VERIFY_FAIL')
