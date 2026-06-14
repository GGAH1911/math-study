import sympy as sp
x = sp.Symbol('x')
f = lambda t: t**2 - sp.Rational(1,3)
f_prime = lambda t: 2*t

# 원래 조건 검증: 3xf(x) = 9∫_1^x f(t)dt + 2x
lhs = 3*x*f(x)
integrand = f(x)
integral_result = sp.integrate(integrand, (x, 1, x))
rhs = 9*integral_result + 2*x

diff = sp.simplify(lhs - rhs)
if diff == 0:
    result = f_prime(1)
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')