from sympy import symbols, integrate, Eq, solve

# f(x) = x + C 형태에서 C를 구하자
C = symbols('C')
t = symbols('t')

# f(t) = t + C이므로
integral_value = integrate(t + C, (t, 0, 2))

# C = 2 + 2C 방정식을 풀기
eq = Eq(C, integral_value)
C_value = solve(eq, C)[0]

# f(x) = x + C_value
def f(x):
    return x + C_value

# 검증: f(x) = x + C_value가 원래 조건을 만족하는지 확인
x = symbols('x')
integral_check = integrate(f(t), (t, 0, 2))
f_x = x + integral_check

# f(x) = x - 2가 f(x) = x + integral값을 만족하는지 확인
if f_x == x + C_value:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')