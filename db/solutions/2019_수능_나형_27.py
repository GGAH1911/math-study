import sympy as sp

CANDIDATE = 22

t = sp.Symbol('t')
k = CANDIDATE

# 위치 함수
x = -sp.Rational(1, 3) * t**3 + 3 * t**2 + k

# 속도 (1차 미분)
v = sp.diff(x, t)

# 가속도 (2차 미분)
a = sp.diff(v, t)

# 가속도가 0인 시각 찾기
accel_zero_times = sp.solve(a, t)

# 가속도가 0인 시각에서의 위치
valid = False
for t_val in accel_zero_times:
    if t_val >= 0:
        x_at_t = x.subs(t, t_val)
        if x_at_t == 40:
            valid = True
            break

if valid:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')