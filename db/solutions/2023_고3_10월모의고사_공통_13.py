import sympy as sp

a = sp.Rational(3, 2)
k = sp.Rational(21, 4)

# 점 P = (1, 13/4)
p_x, p_y = sp.Integer(1), sp.Rational(13, 4)
assert p_y == a**(p_x + 1) + 1, 'P not on f1'
assert p_y == -2*p_x + k, 'P not on line'

# 점 Q = (3, -3/4)
q_x, q_y = sp.Integer(3), sp.Rational(-3, 4)
assert q_y == a**(q_x - 3) - sp.Rational(7, 4), 'Q not on f2'
assert q_y == -2*q_x + k, 'Q not on line'

# 점 R = (-2, -3/4): Q를 지나는 수평선과 y = -a^(x+4) + 3/2 의 교점
r_x, r_y = sp.Integer(-2), sp.Rational(-3, 4)
assert r_y == -a**(r_x + 4) + sp.Rational(3, 2), 'R not on f3'
assert r_y == q_y, 'R not on horizontal through Q'

# 거리 검증
QR = sp.sqrt((q_x - r_x)**2 + (q_y - r_y)**2)
PR = sp.sqrt((p_x - r_x)**2 + (p_y - r_y)**2)

if QR == 5 and PR == 5:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: QR={QR}, PR={PR}')
