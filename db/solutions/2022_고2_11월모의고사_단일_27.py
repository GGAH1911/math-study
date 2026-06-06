CANDIDATE = '25'

from sympy import symbols, limit

x = symbols('x')

# 검증된 함수 정의
# f(x) = -2(x+3) (일차함수)
# g(x) = (x+3)(x+1) (최고차항 계수 1인 이차함수)
f_expr = -2 * (x + 3)
g_expr = (x + 3) * (x + 1)

# 조건 1 검증: lim(x→-3) [f(x)g(x)/(x+3)^2] = 4
cond1_limit = limit(f_expr * g_expr / ((x + 3) ** 2), x, -3)

# 조건 2 검증: lim(x→-3) [(f(x)+g(x))/(x+3)] = -4
cond2_limit = limit((f_expr + g_expr) / (x + 3), x, -3)

# 답 계산: g(2) - f(2)
answer = g_expr.subs(x, 2) - f_expr.subs(x, 2)

# 전체 조건 검증
# (1) 조건1 극한값 = 4
# (2) 조건2 극한값 = -4
# (3) 계산값 = 25
# (4) CANDIDATE 값 = 계산값
is_valid = (
    cond1_limit == 4 and
    cond2_limit == -4 and
    answer == 25 and
    int(CANDIDATE) == answer
)

print('VERIFY_PASS' if is_valid else 'VERIFY_FAIL')