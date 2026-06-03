import math
from sympy import pi, symbols, solve, simplify

# 주어진 조건
r = 6  # 반지름
area = 15 * pi  # 부채꼴의 넓이

# 부채꼴 넓이 공식: S = (1/2) * r^2 * θ
# 중심각 θ를 구함
theta = symbols('theta', positive=True)
area_formula = (1/2) * r**2 * theta

# 넓이 식을 풀어서 θ 구함
solution = solve(area_formula - area, theta)
theta_value = solution[0]

# 네 답 5π/6를 역대입하여 검증
theta_answer = 5 * pi / 6
verify_area = (1/2) * 6**2 * theta_answer

if simplify(verify_area - area) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')