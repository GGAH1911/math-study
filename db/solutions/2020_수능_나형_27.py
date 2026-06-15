from sympy import symbols, expand, solve, Abs

CANDIDATE = 27

t = symbols('t', real=True)

# 주어진 위치 함수
x1 = t**3 - 2*t**2 + 3*t
x2 = t**2 + 12*t

# 속도 함수
v1 = 3*t**2 - 4*t + 3
v2 = 2*t + 12

# 속도가 같아지는 시각
equation = v1 - v2
t_values = solve(equation, t)

# t >= 0인 값만 선택
t_solution = [val for val in t_values if val >= 0][0]

# t_solution에서의 위치
x1_at_t = x1.subs(t, t_solution)
x2_at_t = x2.subs(t, t_solution)

# 거리
distance = abs(x2_at_t - x1_at_t)

# 검증
if distance == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')