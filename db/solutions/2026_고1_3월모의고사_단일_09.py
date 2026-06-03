from sympy import symbols, Rational, solve

x, y = symbols('x y')

# 직선 AB 기울기
A = (-1, 4); B = (2, 3)
slope_AB = Rational(B[1]-A[1], B[0]-A[0])  # -1/3

# 직선 CD 기울기 (a=1)
a = 1
C = (-2, 2); D = (1, a)
slope_CD = Rational(D[1]-C[1], D[0]-C[0])  # -1/3

# 평행 조건 확인
assert slope_AB == slope_CD, 'slopes not equal'

# 직선 CD 방정식: y = slope_CD*(x - C[0]) + C[1]
# x절편
b_val = solve(slope_CD*(x - C[0]) + C[1], x)[0]  # x=4
assert b_val == 4, f'x-intercept mismatch: {b_val}'

# a + b
result = a + b_val
assert result == 5, f'a+b mismatch: {result}'

print('VERIFY_PASS')
