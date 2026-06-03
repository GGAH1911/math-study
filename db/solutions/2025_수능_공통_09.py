from sympy import symbols, integrate, solve
x = symbols('x')
f = 3*x**2 - 16*x - 20
a_val = 10
lhs = integrate(f, (x, -2, a_val))
rhs = integrate(f, (x, -2, 0))
print('VERIFY_PASS' if lhs == rhs else f'VERIFY_FAIL lhs={lhs} rhs={rhs}')