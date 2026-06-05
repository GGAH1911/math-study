from sympy import symbols, limit, diff

x = symbols('x')

# 조건을 만족하는 예제 함수
f_expr = 1 + 6*(x-1) + 2*(x-1)**2
g_expr = 1 + (x-1) + 0.5*(x-1)**2

# 조건 (가) 검증
cond_a = limit((f_expr - g_expr)/(x-1), x, 1)

# 조건 (나) 검증
f_at_1 = f_expr.subs(x, 1)
cond_b = limit((f_expr + g_expr - 2*f_at_1)/(x-1), x, 1)

# g(1) 값
g_at_1 = g_expr.subs(x, 1)

# 우리 답 검증
a = f_at_1
f_prime = diff(f_expr, x).subs(x, 1)
b = f_prime / g_at_1
ab = a * b

# 최종 검증
if cond_a == 5 and cond_b == 7 and ab == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')