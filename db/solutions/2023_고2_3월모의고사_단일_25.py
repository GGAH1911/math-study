from sympy import symbols, sqrt, solve, Eq
import math

CANDIDATE = '3'

# CANDIDATE를 float로 변환
try:
    a = float(CANDIDATE)
except ValueError:
    print("VERIFY_FAIL")
    exit()

# 문제 조건 인코딩:
# f(x) = sqrt(-ax + 1), a > 0
# 정의역: -5 <= x <= -1
# 조건: 이 구간에서 최댓값 = 4

# 조건 1: a > 0 확인
if a <= 0:
    print("VERIFY_FAIL")
    exit()

# 조건 2: sympy를 사용하여 최댓값 조건 검증
# a > 0이면 f(x) = sqrt(-ax + 1)는 감소함수
# 따라서 최댓값은 x = -5에서 발생
# 최댓값 조건: f(-5) = sqrt(5a + 1) = 4

a_sym = symbols('a', positive=True, real=True)
equation = Eq(sqrt(5*a_sym + 1), 4)
solutions = solve(equation, a_sym)

# CANDIDATE가 방정식의 정확한 해인지 확인
epsilon = 1e-9
found_solution = any(abs(float(sol) - a) < epsilon for sol in solutions)

if not found_solution:
    print("VERIFY_FAIL")
    exit()

# 추가 검증: 실제로 a = CANDIDATE일 때 최댓값이 4인지 확인
f_at_minus5 = math.sqrt(5 * a + 1)  # x = -5에서의 값 (최댓값)
f_at_minus1 = math.sqrt(a + 1)      # x = -1에서의 값 (최솟값)

# 최댓값이 4인지, 그리고 감소함수인지 확인
if abs(f_at_minus5 - 4.0) < epsilon and f_at_minus1 < f_at_minus5:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")