from sympy import Rational, Abs

def f(x_val):
    from sympy import Abs
    ax = abs(x_val)
    return 1 if ax >= 1 else ax

def orig_eq(x_val, y):
    return y**3 - y**2 - x_val**2 * y + x_val**2

x1 = Rational(-4, 3)
x2 = Rational(0)
x3 = Rational(1, 2)

f1, f2, f3 = f(x1), f(x2), f(x3)

eq1 = orig_eq(x1, f1)
eq2 = orig_eq(x2, f2)
eq3 = orig_eq(x3, f3)

total = f1 + f2 + f3

max_ok = all(f(x) <= 1 for x in [Rational(k,10) for k in range(-20,21)])
min_ok = f(Rational(0)) == 0

if eq1 == 0 and eq2 == 0 and eq3 == 0 and total == Rational(3,2) and max_ok and min_ok:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL eq1={eq1} eq2={eq2} eq3={eq3} total={total} max_ok={max_ok} min_ok={min_ok}')
