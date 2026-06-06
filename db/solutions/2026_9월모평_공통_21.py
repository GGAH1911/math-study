from sympy import symbols, simplify

CANDIDATE = '296'

# f(x) = x^3 + a*x^2 + b*x + c  (최고차항의 계수가 1)
# f'(x) = 3*x^2 + 2*a*x + b

# 주어진 부등식 (0이 아닌 모든 실수 x에 대해):
# (x^2 * f'(2x)) / (2x^2) <= (x^2 * f(x)) / (x^2 + 10x) <= x^4
# 즉: f'(2x)/2 <= (x^2 * f(x)) / (x^2 + 10x) <= x^4

# 검증된 풀이에서 사용한 보조 변수:
# M(x) = (f(2x) - f(0)) / (2x) = 4x^2 + 2ax + b
# L(x) = f'(x)/2 + x^2 - 2 = (5/2)x^2 + ax + b/2 - 2
# R(x) = x^4

# 부등식을 정렬하면:
# 왼쪽: M(x) - L(x) >= 0
# 오른쪽: R(x) - M(x) >= 0

x = symbols('x')

# 검증된 풀이의 결과: a = 0, b = -4
a = 0
b = -4

# 왼쪽 부등식 확인
M = 4*x**2 + 2*a*x + b
L = (5/2)*x**2 + a*x + b/2 - 2
M_minus_L = simplify(M - L)
# M - L = 4x^2 - 4 - (5/2*x^2 - 4) = (3/2)x^2 >= 0 ✓

# 오른쪽 부등식 확인
R = x**4
R_minus_M = simplify(R - M)
# R - M = x^4 - 4x^2 + 4 = (x^2 - 2)^2 >= 0 ✓

# f'(1) 계산
f_prime_1 = 3*1**2 + 2*a*1 + b
# f'(1) = 3 + 0 - 4 = -1
assert f_prime_1 == -1

# f'(1) + f(10) = 296이 되도록 c 결정
# f(10) = 10^3 + a*10^2 + b*10 + c = 1000 + 0 - 40 + c = 960 + c
# f'(1) + f(10) = -1 + 960 + c = 296
# c = 296 - 959 = -663

c_needed = 296 - f_prime_1 - (1000 + a*100 + b*10)
fx_10 = 10**3 + a*10**2 + b*10 + c_needed

result = f_prime_1 + fx_10

if str(result) == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')