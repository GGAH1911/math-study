import sympy as sp
from sympy import symbols, cos, sin, pi, solve, simplify, sqrt

# 원래 문제의 조건: cos(-theta) + sin(pi + theta) = 3/5
# 즉, cos(theta) - sin(theta) = 3/5

theta = symbols('theta', real=True)

# 원래 조건식
condition = cos(theta) - sin(theta) - sp.Rational(3, 5)

# 주어진 답: sin(theta) * cos(theta) = 8/25
candidate_answer = sp.Rational(8, 25)

# cos(theta) - sin(theta) = 3/5 에서
# (cos(theta) - sin(theta))^2 = 9/25
# cos^2(theta) - 2*sin(theta)*cos(theta) + sin^2(theta) = 9/25
# 1 - 2*sin(theta)*cos(theta) = 9/25
# 2*sin(theta)*cos(theta) = 16/25
# sin(theta)*cos(theta) = 8/25

# 검증: sin(theta) - cos(theta) = 3/5 조건과
# sin(theta)*cos(theta) = 8/25 를 동시에 만족하는 sin, cos가 존재하는가?

sin_theta, cos_theta = symbols('sin_theta cos_theta', real=True)

eq1 = cos_theta - sin_theta - sp.Rational(3, 5)  # 원래 조건
eq2 = sin_theta * cos_theta - sp.Rational(8, 25)  # 검증할 답
eq3 = sin_theta**2 + cos_theta**2 - 1  # 피타고라스 항등식

solutions = solve([eq1, eq2, eq3], [sin_theta, cos_theta])

if solutions:
    for sol in solutions:
        s, c = sol
        # 각 해에 대해 원래 조건을 검증
        check_condition = simplify(c - s - sp.Rational(3, 5))
        check_product = simplify(s * c - sp.Rational(8, 25))
        check_identity = simplify(s**2 + c**2 - 1)
        
        if check_condition == 0 and check_product == 0 and check_identity == 0:
            print('VERIFY_PASS')
            exit()
    print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')