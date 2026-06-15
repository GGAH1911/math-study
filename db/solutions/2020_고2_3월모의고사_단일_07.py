from sympy import symbols, Eq, solve, Rational

a = symbols('a')

# 1:2 내분점 공식
x_div = Rational(1*6 + 2*0, 1+2)  # = 2
y_div = (1*0 + 2*a) / (1+2)       # = 2a/3

# y = -x 조건 적용
eq = Eq(y_div, -x_div)
sol = solve(eq, a)[0]

# a = -3 검증: 내분점 (2, -2)가 y=-x 위에 있는지 확인
a_val = sol
x_pt = 2
y_pt = (2*a_val) / 3

if y_pt == -x_pt and a_val == -3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
