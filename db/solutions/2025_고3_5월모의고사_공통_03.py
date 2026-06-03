from sympy import sqrt, Rational, simplify

k = 1 / sqrt(2)
a2 = k**2
a3 = k**3
a4 = k**4

lhs = a2 * (k**2 + 1)
rhs = 3 * a4

cond_ok = simplify(lhs - rhs) == 0
k_positive = k > 0
a3_val = simplify(a3)
expected = sqrt(2) / 4
a3_ok = simplify(a3_val - expected) == 0

if cond_ok and k_positive and a3_ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
