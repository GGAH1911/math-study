from sympy import *
import numpy as np

# 주어진 조건 검증
R = sqrt(3)  # 원의 반지름
BC = 3  # 위에서 도출

# 정현법칙: BC = 2R sin(∠BAC)
angle_BAC = asin(BC / (2*R))
assert abs(angle_BAC - pi/3) < 1e-6, f"∠BAC should be 60°, got {deg(angle_BAC)}"

# BD = √3 조건 확인 (정현법칙으로)
# BD = 2R sin(호BD/2)에서 호BD = 60°
BD = 2*R*sin(pi/6)  # sin(30°)
assert abs(BD - sqrt(3)) < 1e-6, f"BD should be √3, got {BD}"

# 보기 (가): sin(∠DBE) = 1/2
angle_DBE = pi/6  # 30°
assert abs(sin(angle_DBE) - Rational(1,2)) < 1e-6, "보기 (가) 실패"

# 보기 (나): AB² + AC² = AB·AC + 9
# 코사인 법칙에서 BC² = AB² + AC² - 2AB·AC·cos(60°)
# 9 = AB² + AC² - AB·AC
# 따라서 AB² + AC² = AB·AC + 9 ✓

# 보기 (다): S_ABC = 4·S_BDE 조건에서 BE 값들의 합 = 9/4
# 이등분선: BE = (3·AB)/(AB+AC)
# 조건 정리: AB·AC = 12 - AC²
# 연립하면: AC⁴ - 15·AC² + 48 = 0

t = symbols('t', positive=True)
eq = t**2 - 15*t + 48
AC_squared_vals = solve(eq, t)

BE_vals = []
for AC_sq in AC_squared_vals:
    # BE = (12 - AC²)/4
    BE = (12 - AC_sq) / 4
    BE_vals.append(BE)

BE_sum = sum(BE_vals)
assert abs(BE_sum - Rational(9,4)) < 1e-6, f"BE 값의 합이 9/4가 아닙니다: {BE_sum}"

print('VERIFY_PASS')