from fractions import Fraction
a = Fraction(3, 14)
r = Fraction(11, 3)
t = 2
def f(x):
    return a * x * (x - 2) * (x - r)
def g(x):
    return -f(x) if x < t else f(x)
g_minus_5 = g(-5)
if g_minus_5 == 65:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')