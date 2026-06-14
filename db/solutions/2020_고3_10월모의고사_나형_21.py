from sympy import symbols, log, nsolve, sqrt, Rational, N

# 변수 정의
x = symbols('x', real=True, positive=True)

# 원래 문제의 방정식들
# x ∈ (0,1)에서: 2^(-x) = -log_2(x)  →  2^(-x) + log_2(x) = 0
eq1 = 2**(-x) + log(x, 2)

# x ∈ (1,∞)에서: 2^(-x) = log_2(x)  →  2^(-x) - log_2(x) = 0
eq2 = 2**(-x) - log(x, 2)

# 첫 번째 교점 구하기
x1 = nsolve(eq1, 0.7)
y1 = 2**(-x1)

# 두 번째 교점 구하기
x2 = nsolve(eq2, 1.5)
y2 = 2**(-x2)

# 조건값 정의
half = Rational(1, 2)
sqrt2 = sqrt(2)
sqrt2_half = sqrt2 / 2
cbrt2 = 2**(Rational(1, 3))
bound = (3*sqrt2 - 2) / 6

# 보기 ㄱ 검증: 1/2 < x1 < sqrt(2)/2
check_a = (N(half) < N(x1)) and (N(x1) < N(sqrt2_half))

# 보기 ㄴ 검증: 2^(1/3) < x2 < sqrt(2)
check_b = (N(cbrt2) < N(x2)) and (N(x2) < N(sqrt2))

# 보기 ㄷ 검증: y1 - y2 < (3*sqrt(2) - 2) / 6
check_c = (N(y1 - y2) < N(bound))

# 원래 방정식이 실제로 만족되는지 검증
eq1_residual = abs(N(2**(-x1) + log(x1, 2)))
eq2_residual = abs(N(2**(-x2) - log(x2, 2)))
eq1_satisfied = eq1_residual < 1e-10
eq2_satisfied = eq2_residual < 1e-10

# 모든 조건 확인
if check_a and check_b and check_c and eq1_satisfied and eq2_satisfied:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')