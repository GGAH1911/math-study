from sympy import symbols, solve, Interval
x = symbols('x')
a = 4

# 조건 Q의 해
Q_expr = x**2 - 2*x - 8
Q_roots = solve(Q_expr, x)
print(f'Q의 판별식 값: {Q_roots}')

# Q가 참인 범위
Q_range = Interval(-2, 4)

# P가 참인 범위
P_range = Interval(-a, a)

# Q_range가 P_range에 포함되는지 확인
if Q_range.is_subset(P_range):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')