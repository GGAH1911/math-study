from sympy import *

c_sym = symbols('c', positive=True)

# f(c) = 10 - c (가), g(c) = 50 - 10c (나)
f = lambda x: 10 - x
g = lambda x: 50 - 10*x

# Discriminant D = c^2 + 20c - 100 >= 0
D = f(c_sym)**2 - 4*g(c_sym)
D_exp = expand(D)  # c^2 + 20c - 100

# k = positive root of D = 0
roots = solve(D_exp, c_sym)
k = [r for r in roots if r > 0][0]  # 10*(sqrt(2)-1)

# f(9/2), g(9/2)
f_val = f(Rational(9, 2))  # 11/2
g_val = g(Rational(9, 2))  # 5

# Formula: k/25 * f(9/2) * g(9/2)
result = simplify(k / 25 * f_val * g_val)

expected = 11*(sqrt(2) - 1)

# Also verify k is 10*(sqrt(2)-1)
k_check = simplify(k - 10*(sqrt(2)-1))

if k_check == 0 and simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'k={k}, result={result}, expected={expected}')
