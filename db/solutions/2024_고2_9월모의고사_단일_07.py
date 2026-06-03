import math
from sympy import pi, symbols, simplify

# 주어진 조건
theta = pi / 4  # 중심각
area = 18 * pi  # 넓이

# 부채꼴 넓이 공식: A = (1/2) * r^2 * theta
# 18π = (1/2) * r^2 * (π/4)
# r^2 = 144, r = 12
r = 12

# 호의 길이: l = r * theta
l = r * theta
l_simplified = simplify(l)

# 검증: 넓이 공식에서 r=12, theta=π/4 대입
area_check = simplify((1/2) * r**2 * theta)

if simplify(area_check - area) == 0 and l_simplified == 3*pi:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')