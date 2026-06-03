from sympy import symbols, solve, sqrt, simplify

# 타원 위의 점 (a, b) = (4, 2)
a, b = 4, 2

# 타원 방정식에서 점 (a, b)가 만족하는지 확인
ellipse_check = a**2 / 32 + b**2 / 8
assert abs(ellipse_check - 1) < 1e-10, f'Point not on ellipse: {ellipse_check}'

# 접선 방정식: (ax)/32 + (by)/8 = 1
# 점 (8, 0)이 접선 위에 있는지 확인
tangent_check = (a * 8) / 32 + (b * 0) / 8
assert abs(tangent_check - 1) < 1e-10, f'Point (8,0) not on tangent: {tangent_check}'

# 제1사분면 확인
assert a > 0 and b > 0, 'Point not in first quadrant'

print('VERIFY_PASS')