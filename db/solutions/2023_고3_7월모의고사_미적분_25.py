from sympy import symbols, exp, solve, Eq, Rational

x_val, y_val = 0, 1

# 1. 점이 곡선 위에 있는지 확인
lhs = 2 * exp(x_val + y_val - 1)
rhs = 3 * exp(x_val) + x_val - y_val
assert abs(float(lhs - rhs)) < 1e-10, 'Point not on curve'

# 2. 음함수 미분: 2e^{x+y-1}(1+y') = 3e^x + 1 - y'
# 점 (0,1) 대입
dydx = symbols('dydx')
eq = Eq(2 * exp(x_val + y_val - 1) * (1 + dydx), 3 * exp(x_val) + 1 - dydx)
sol = solve(eq, dydx)

answer = Rational(2, 3)
if sol and abs(float(sol[0]) - float(answer)) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')