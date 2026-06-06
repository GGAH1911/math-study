CANDIDATE = '15'

from sympy import symbols, integrate, diff

x = symbols('x')

# 문제 조건: f'(x) = 8x^3 + 6x^2
f_prime = 8*x**3 + 6*x**2

# 부정적분으로 f(x) 구하기
f_integral = integrate(f_prime, x)  # 2x^4 + 2x^3

# 초기조건 f(0) = -1으로 상수 결정
# f(x) = 2x^4 + 2x^3 + C에서
# f(0) = 2(0)^4 + 2(0)^3 + C = C = -1
C = -1
f_x = f_integral + C  # f(x) = 2x^4 + 2x^3 - 1

# 원래 조건들이 만족되는지 검증
assert diff(f_x, x) == f_prime, "도함수 검증 실패"
assert f_x.subs(x, 0) == -1, "초기조건 f(0) = -1 검증 실패"

# f(-2) 계산
# f(-2) = 2(-2)^4 + 2(-2)^3 - 1 = 2(16) + 2(-8) - 1 = 32 - 16 - 1 = 15
f_at_minus_2 = f_x.subs(x, -2)

# CANDIDATE 검증
if int(f_at_minus_2) == int(CANDIDATE):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")