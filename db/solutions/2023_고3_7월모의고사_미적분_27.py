from sympy import Rational, sqrt, simplify

# 원래 삼각형: AB1=AC1=sqrt(17), B1C1=2
# 좌표: A=(0,4), B1=(-1,0), C1=(1,0)
AB1_sq = 1 + 16  # =17 -> sqrt(17)
B1C1 = 2
assert AB1_sq == 17 and B1C1 == 2, 'VERIFY_FAIL: 삼각형 조건'

# D1 = (0, d), d=3/5 결정
d = Rational(3, 5)
# B2 = D1 + CW90(B1-D1) = (-d, d+1)
B2 = (-d, d + 1)
# B2가 AB1 위 확인: 매개변수 t=d 일 때 (-t, 4-4t)
t = d
assert (-t, 4 - 4*t) == B2, 'VERIFY_FAIL: B2 not on AB1'

# B1D1^2 = B2D1^2
l2_B1 = Rational(1) + d**2
l2_B2 = d**2 + Rational(1)
assert l2_B1 == l2_B2 == Rational(34, 25), 'VERIFY_FAIL: 길이 불일치'

# 수직 확인: (B1-D1)·(B2-D1) = 0
dot = (-1)*(-d) + (-d)*(1)
assert dot == 0, 'VERIFY_FAIL: 각도 불일치'

# S1 = 2*(l^2/2) = l^2
S1 = l2_B1
assert S1 == Rational(34, 25), 'VERIFY_FAIL: S1'

# 닮음비 k=3/5, 넓이 공비 k^2=9/25
AB2_sq = (Rational(3,5))**2 + (Rational(12,5))**2  # (3/5)^2+(12/5)^2 = 153/25
k_sq = AB2_sq / Rational(17)  # = (153/25)/17 = 9/25
assert k_sq == Rational(9, 25), f'VERIFY_FAIL: k^2={k_sq}'

# 극한
lim_val = S1 / (1 - k_sq)
lim_val = simplify(lim_val)
if lim_val == Rational(17, 8):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL:', lim_val)
