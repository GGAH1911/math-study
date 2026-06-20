from sympy import symbols, expand, factor, diff

CANDIDATE = 10

# 원래 곡선 정의
x = symbols('x')
curve = x**3 - 6*x**2 + 6

# 도함수 구하기
curve_prime = diff(curve, x)

# 점 (1, 1)에서의 기울기
slope_at_1 = curve_prime.subs(x, 1)

# 점 (1, 1)에서의 접선 방정식: y - 1 = slope_at_1 * (x - 1)
# y = slope_at_1 * x + (1 - slope_at_1)
tangent_intercept = 1 - slope_at_1

# 접선이 (0, a)를 지나므로 a = tangent_intercept
a_value = tangent_intercept

# 검증: 접선과 곡선의 교점에서 x=1이 중근인지 확인
eq = curve - (slope_at_1 * x + tangent_intercept)
factored = factor(eq)

if a_value == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')