from sympy import symbols, diff, Function, Eq, solve
import sympy as sp

# f(x)는 다항함수, f(3) = 2, f'(3) = 0을 만족
# g(x) = (x^2 - 2x)f(x)
# g'(x) = (2x - 2)f(x) + (x^2 - 2x)f'(x)

x = symbols('x')

# x^2 - 2x 항
quad_term = x**2 - 2*x
quad_term_deriv = diff(quad_term, x)  # 2x - 2

# 조건: f(3) = 2, f'(3) = 0
f_3 = 2
f_prime_3 = 0

# g'(3) = (2*3 - 2)*f(3) + (3^2 - 2*3)*f'(3)
coeff1 = quad_term_deriv.subs(x, 3)  # 2*3 - 2 = 4
coeff2 = quad_term.subs(x, 3)  # 3^2 - 2*3 = 3

g_prime_3 = coeff1 * f_3 + coeff2 * f_prime_3
result = g_prime_3

if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')