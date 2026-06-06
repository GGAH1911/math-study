CANDIDATE = '11'

from sympy import symbols, diff, solve

# 문제에서 주어진 함수: f(x) = x^3 - 3x + 12
x = symbols('x')
f = x**3 - 3*x + 12

# 1차 도함수: f'(x) = 3x^2 - 3
f_prime = diff(f, x)

# 2차 도함수: f''(x) = 6x
f_double_prime = diff(f_prime, x)

# 극값 후보: f'(x) = 0인 점들 (조건: f'(a) = 0)
critical_points = solve(f_prime, x)

# 극소 조건을 만족하는 점 찾기: f''(a) > 0 (극소 판정)
a = None
for cp in critical_points:
    second_deriv_value = f_double_prime.subs(x, cp)
    if second_deriv_value > 0:  # 극소 조건
        a = cp
        break

# 극소점에서 함수값 계산: f(a)
f_a = f.subs(x, a)

# 문제에서 구하는 값: a + f(a)
result = a + f_a

# CANDIDATE 검증 (문제 조건에 의존)
candidate_int = int(CANDIDATE)
if result == candidate_int:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')