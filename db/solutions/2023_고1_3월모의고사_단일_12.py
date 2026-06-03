from sympy import Rational

def f(val):
    p = Rational(-3, 10)
    h = Rational(9, 2)
    q = Rational(187, 40)
    return p * (val - h)**2 + q

# 원래 조건: A, B, C, D 모두 포물선 위
assert f(1) == 1, 'A fail'
assert f(8) == 1, 'B fail'
assert f(6) == 4, 'C fail'

a_val = Rational(3)
b_val = Rational(4)
assert f(a_val) == b_val, 'D not on parabola'
assert (a_val, b_val) != (6, 4), 'D must differ from C'

# AB // CD 확인: 외적 = 0
dx_AB, dy_AB = 8-1, 1-1          # (7, 0)
dx_CD, dy_CD = int(a_val)-6, int(b_val)-4  # (-3, 0)
cross = dx_AB * dy_CD - dy_AB * dx_CD

# a+b 확인
result = int(a_val) + int(b_val)

if cross == 0 and dx_CD != 0 and result == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')