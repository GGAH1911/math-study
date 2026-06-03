from sympy import symbols, integrate, Abs, Rational
t = symbols('t')
v = t**2 - 4*t + 3
a_val = 3  # 방향전환 조건에서 a=3
# 방향전환 시각 확인: v(1)=0, v(a)=0
assert v.subs(t, 1) == 0, 'v(1) != 0'
assert v.subs(t, a_val) == 0, 'v(a) != 0'
# 1 < t < a 구간에서 v < 0인지 확인
import sympy as sp
mid = (1 + a_val) / 2  # t=2
assert float(v.subs(t, mid)) < 0, 'v(mid) should be negative'
# 이동 거리 계산
dist = integrate(Abs(v), (t, 0, a_val))
expected = Rational(8, 3)
if dist == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {dist}, expected {expected}')
