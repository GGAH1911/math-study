from sympy import symbols, solve, Eq

# 변수 정의
a, b = symbols('a b', positive=True, real=True)

# 포물선 방정식: y^2 - 4y - ax + 4 = 0
# 정리: (y-2)^2 = ax
# 표준형 (y-k)^2 = 4p(x-h)에서
# 꼭짓점 (h, k) = (0, 2)
# 4p = a이므로 p = a/4
# 초점: (h+p, k) = (a/4, 2)

# 초점이 (3, b)라는 조건
eq1 = Eq(a/4, 3)  # x 좌표
eq2 = Eq(2, b)    # y 좌표

# 풀이
sol_a = solve(eq1, a)[0]
sol_b = solve(eq2, b)[0]

result = sol_a + sol_b

# 검증: 구한 a, b로 포물선 방정식 확인
x_focus = sol_a / 4
y_focus = sol_b

if x_focus == 3 and y_focus == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')