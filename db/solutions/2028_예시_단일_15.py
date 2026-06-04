from sympy import symbols, diff, solve, Eq

t = symbols('t', real=True, positive=True)

# 원래 문제의 식
x1 = t**3 + 3*t - 5
x2 = 6*t + 1

# 속도
v1 = diff(x1, t)
v2 = diff(x2, t)

# 조건: v1 = 5 * v2
eq = Eq(v1, 5*v2)
t_value = solve(eq, t)
t_value = [val for val in t_value if val >= 0][0]

# 가속도
a1 = diff(v1, t)
a_at_t = a1.subs(t, t_value)

# 검증: 주어진 답이 18인지 확인
if a_at_t == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')