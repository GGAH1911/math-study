from sympy import *

CANDIDATE = 3

# 주어진 조건: ∫₀ˣ f(t)dt = ln(x) + ln(x²) + c
# 우변 정리: ln(x) + ln(x²) + c = 3ln(x) + c
# 양변을 x로 미분하면: f(x) = 3/x

x = symbols('x', positive=True, real=True)

# f(x) = 3/x 정의
f_x = 3 / x

# f(1) 계산
f_at_1 = f_x.subs(x, 1)

# 미적분학 기본정리 검증: f(x) = d/dx[3*ln(x) + c]
right_side = diff(3*ln(x), x)
assert right_side == f_x, 'Differentiation check failed'

# CANDIDATE 검증
if f_at_1 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')