from sympy import *

CANDIDATE = 29

# 문제: 0 ≤ x ≤ 6에서 함수 y = log_{1/3}(x+3) + 30의 최댓값을 구하시오
# 원래 함수를 sympy로 표현
x = symbols('x', real=True)
y = log(x + 3, Rational(1, 3)) + 30

# 함수의 도함수 계산
dy_dx = diff(y, x)
# dy/dx = 1/((x+3)*ln(1/3)) = 1/((x+3)*(-ln(3))) < 0
# ln(1/3) < 0이므로 dy/dx는 항상 음수 → 함수는 감소함수

# 감소함수이므로 정의역 [0, 6]에서 최댓값은 x=0에서 달성
maximum_value = y.subs(x, 0)
# maximum_value = log(3, 1/3) + 30 = -1 + 30 = 29

# CANDIDATE 검증
if abs(maximum_value - CANDIDATE) < 1e-10:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")