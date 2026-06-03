from sympy import symbols, integrate, Rational, simplify

x, t = symbols('x t')

C = Rational(-1, 2)
f_x = Rational(3, 2)*x**2 + C
f_t = Rational(3, 2)*t**2 + C

lhs = integrate(f_t, (t, 1, x))
rhs = x * f_x - x**3

diff = simplify(lhs - rhs)

f2 = f_x.subs(x, 2)

if diff == 0 and f2 == Rational(11, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('diff =', diff, 'f(2) =', f2)
