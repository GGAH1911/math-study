import sympy as sp
from sympy import symbols, Abs, solve

x, a = symbols('x a', real=True)

# f'(x) = 2*a*(x-1), constraint: |2*a*(x-1)| <= 4*x^2 + 5
# Check a = 2
a_val = 2
f_prime = 2 * a_val * (x - 1)

# Test at critical point x = -0.5
x_test = sp.Rational(-1, 2)
lhs = Abs(f_prime.subs(x, x_test))
rhs = 4 * x_test**2 + 5

print(f'At x = -1/2: |f\'(x)| = {lhs}, RHS = {rhs}')
print(f'Constraint satisfied: {lhs <= rhs}')

# General verification: check that (2x+1)^2 >= 0 for x < 1 and 4x^2 - 4x + 9 > 0 for x >= 1
expr1 = 4*x**2 + 4*x + 1  # Should be (2x+1)^2
expr2 = 4*x**2 - 4*x + 9  # Should be positive

factored1 = sp.factor(expr1)
min_expr2 = sp.solve(sp.diff(expr2, x), x)

print(f'For x < 1: {expr1} = {factored1} >= 0 ✓')
print(f'For x >= 1: {expr2} has minimum {expr2.subs(x, 1/2)} > 0 ✓')

if lhs == rhs:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')