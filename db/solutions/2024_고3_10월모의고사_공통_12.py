from sympy import *

t = symbols('t')
a_val = 3

# 원래 문제의 속도 함수
v1 = -3*t**2 + a_val*t
v2 = -t + 1

# 위치 함수 (원점 출발, 적분상수=0)
x_P = integrate(v1, t)  # -t^3 + (a/2)*t^2
x_Q = integrate(v2, t)  # -t^2/2 + t

# 만나는 조건: x_P = x_Q, t > 0
diff_pos = x_P - x_Q  # = -t*(t-1)^2 when a=3
all_roots = solve(diff_pos, t)
positive_roots = sorted([r for r in all_roots if r > 0])

# 정확히 하나의 양의 근 (t=1)
meets_once = (len(positive_roots) == 1 and positive_roots[0] == 1)

# t=1에서 위치 일치 확인
meeting_ok = (x_P.subs(t, 1) == x_Q.subs(t, 1))

# t=0~3 이동 거리: v1은 t=1에서 부호 바뀜
d1 = integrate(v1, (t, 0, 1))    # 양의 방향
d2 = integrate(-v1, (t, 1, 3))   # 음의 방향 → 절댓값
total_dist = d1 + d2
expected = Rational(29, 2)

if meets_once and meeting_ok and total_dist == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'positive_roots={positive_roots}, meeting_ok={meeting_ok}')
    print(f'total_dist={total_dist}, expected={expected}')
