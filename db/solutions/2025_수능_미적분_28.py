from sympy import *

x = symbols('x')

# f'(x) as given in the problem
f_prime = -x + exp(1 - x**2)
f_double_prime = diff(f_prime, x)

# g'(1) = -1/2 * f''(1)
f_pp_at_1 = f_double_prime.subs(x, 1)
g_prime_1 = Rational(-1, 2) * f_pp_at_1

# g(1) = integral_0^1 x * f'(x) dx  (derived via IBP since f'(1)=0)
g_1 = integrate(x * f_prime, (x, 0, 1))

result = simplify(g_1 + g_prime_1)
expected = Rational(1,2)*E + Rational(2,3)

if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', result, 'expected', expected)
