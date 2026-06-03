from sympy import symbols, integrate, diff, simplify

x, t, a_sym = symbols('x t a')

# Given: f(x) = 3x^2 + 2, a = 3
a_val = 3
f = 3*x**2 + 2
f_t = f.subs(x, t)

# Compute integral constant C = integral_0^1 f'(t) dt
C = integrate(diff(f_t, t), (t, 0, 1))

# Check: x*f(x) == a*x^3 + 2*x - 3 + C for all x
lhs = x * f
rhs = a_val * x**3 + 2*x - 3 + C

diff_check = simplify(lhs - rhs)

# Compute the definite integral
result = integrate(f, (x, 0, 2))

if diff_check == 0 and result == 12:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: diff={diff_check}, integral={result}')
