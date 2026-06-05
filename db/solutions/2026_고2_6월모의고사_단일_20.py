import sympy as sp
from sympy import tan, pi, simplify, solve

# 정의된 값
a_val = sp.Rational(20, 13) * pi
b_val = sp.Rational(28, 13) * pi
c_val = 4*pi - a_val

# 함수값 계산
f_a = 4 * tan(a_val / 4)
f_c = 2 * tan(c_val / 4)

# 조건 (가) 검증: a + c = 4π
check_condition_ga = simplify(a_val + c_val)
print(f'Condition (가): a + c = {check_condition_ga} (should be 4π)')
assert check_condition_ga == 4*pi, 'Condition (가) failed'

# 기울기 검증
slope = (f_c - f_a) / (c_val - a_val)
slope_simplified = simplify(slope)
print(f'Slope (simplified): {slope_simplified}')

# 직선 방정식이 B(b, 0)을 지나는지 검증
# y - f_a = slope * (x - a) 형태로, x=b, y=0을 대입
residual = 0 - f_a - slope_simplified * (b_val - a_val)
residual_simplified = simplify(residual)
print(f'Line equation check at B: {residual_simplified} (should be 0)')
assert residual_simplified == 0, 'Line equation check failed'

# 조건 (나) 검증: 넓이 비 = 7:3
area_AOB = sp.Rational(1, 2) * b_val * abs(f_a)
area_BCP = sp.Rational(1, 2) * abs(4*pi - b_val) * abs(f_c)

area_AOB_simplified = simplify(area_AOB)
area_BCP_simplified = simplify(area_BCP)
ratio = simplify(area_AOB_simplified / area_BCP_simplified)
print(f'Area AOB: {area_AOB_simplified}')
print(f'Area BCP: {area_BCP_simplified}')
print(f'Area ratio AOB/BCP: {ratio} (should be 7/3)')
assert ratio == sp.Rational(7, 3), 'Area ratio check failed'

print('\nVERIFY_PASS')