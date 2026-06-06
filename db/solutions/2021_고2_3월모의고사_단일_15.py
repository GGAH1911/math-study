from sympy import *
A = (1, 3)
B = (5, Rational(-5, 3))
C = (-5, Rational(5, 3))

# 조건 검증
OA_slope = 3
OB_slope = Rational(-5, 3) / 5
assert OA_slope * OB_slope == -1, 'OA와 OB가 수직이 아님'

# B와 C가 직선 y=3x에 대해 대칭 검증
midpoint = ((5 - 5) / 2, (Rational(-5, 3) + Rational(5, 3)) / 2)
assert midpoint == (0, 0), 'B와 C의 중점이 원점이 아님'
BC_slope = (Rational(5, 3) - Rational(-5, 3)) / (-5 - 5)
assert OA_slope * BC_slope == -1, 'BC가 OA에 수직이 아님'

# 직선 AC의 방정식 검증
m_AC = (Rational(5, 3) - 3) / (-5 - 1)
y_intercept = 3 - m_AC * 1
assert y_intercept == Rational(25, 9), '절편 계산 오류'

# A와 C가 직선 위에 있는지 확인
assert 3 == m_AC * 1 + y_intercept, 'A가 직선 위에 없음'
assert Rational(5, 3) == m_AC * (-5) + y_intercept, 'C가 직선 위에 없음'

print('VERIFY_PASS')