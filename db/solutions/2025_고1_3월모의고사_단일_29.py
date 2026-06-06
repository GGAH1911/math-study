import sympy as sp
x = sp.Symbol('x')
a, p, q = -1, sp.Rational(7, 4), sp.Rational(121, 16)
f = a * (x - p)**2 + q

# 검증: 세 점을 지나는가?
check_A = f.subs(x, 3)
check_B = f.subs(x, 0)
check_C = f.subs(x, -1)

if check_A == 6 and check_B == sp.Rational(9, 2) and check_C == 0:
    k = q
    result = 16 * k
    if result == 121:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')