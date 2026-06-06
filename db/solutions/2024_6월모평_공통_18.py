CANDIDATE = '6'

from sympy import symbols, Eq, solve

a, b, c = symbols('a b c', real=True)

# 원래 문제 조건을 방정식으로 인코딩:
# f(x) = a*x^3 + b*x + c (삼차함수, 상수항 포함)
# 조건 1: f'(1) = 0 (x=1에서 극소)
# 조건 2: f(1) = -2 (극솟값이 -2)
# 조건 3: f(-1) = CANDIDATE (극댓값이 정답)

# f'(x) = 3*a*x^2 + b에서
eq1 = Eq(3*a + b, 0)  # f'(1) = 0

# f(x) = a*x^3 + b*x + c에서
eq2 = Eq(a + b + c, -2)  # f(1) = -2 (극솟값 조건)

# 극댓값 조건
eq3 = Eq(-a - b + c, int(CANDIDATE))  # f(-1) = 6 (극댓값)

# 연립 방정식 풀이
solution = solve((eq1, eq2, eq3), (a, b, c))
a_val = float(solution[a])
b_val = float(solution[b])
c_val = float(solution[c])

# 원래 문제 조건으로 역대입 검증
f_prime_at_1 = 3*a_val + b_val
f_at_1 = a_val + b_val + c_val
f_at_minus1 = -a_val - b_val + c_val
f_double_prime_at_1 = 6*a_val

# 모든 조건이 만족되는지 확인
cond1_pass = abs(f_prime_at_1 - 0) < 1e-9  # f'(1) = 0
cond2_pass = abs(f_at_1 - (-2)) < 1e-9  # f(1) = -2
cond3_pass = abs(f_at_minus1 - int(CANDIDATE)) < 1e-9  # f(-1) = CANDIDATE
cond4_pass = f_double_prime_at_1 > 0  # f''(1) > 0 (극소)

if cond1_pass and cond2_pass and cond3_pass and cond4_pass:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')