import sympy as sp
from sympy import symbols, integrate, solve, Abs

CANDIDATE = 8

t = symbols('t', real=True)
v = -3*t**2 + 12*t - 9

# 위치함수 구하기 (초기조건 x(0)=0)
x = integrate(v, t)

# 속도가 0이 되는 시각
velocity_zeros = solve(v, t)
print(f"속도 0인 시각: {velocity_zeros}")
first_change = min(t_val for t_val in velocity_zeros if t_val > 0)
print(f"첫 방향 전환: t={first_change}")

# 위치 A
A_position = x.subs(t, first_change)
print(f"위치 A: {A_position}")

# A로 돌아오는 시각
return_times = solve(x - A_position, t)
print(f"x(t)={A_position}인 시각: {return_times}")
return_time = [tv for tv in return_times if tv > first_change][0]
print(f"A로 돌아오는 시각: t={return_time}")

# 중간에 방향이 바뀌는 시각
middle_change = [tv for tv in velocity_zeros if tv > first_change][0]
print(f"중간 방향 전환: t={middle_change}")

# 이동 거리 계산
pos_at_first = x.subs(t, first_change)
pos_at_middle = x.subs(t, middle_change)
pos_at_return = x.subs(t, return_time)

dist1 = Abs(pos_at_middle - pos_at_first)
dist2 = Abs(pos_at_return - pos_at_middle)
total_distance = dist1 + dist2

print(f"\n위치: t={first_change}에서 {pos_at_first}")
print(f"위치: t={middle_change}에서 {pos_at_middle}")
print(f"위치: t={return_time}에서 {pos_at_return}")
print(f"\n거리 ({first_change}~{middle_change}): {dist1}")
print(f"거리 ({middle_change}~{return_time}): {dist2}")
print(f"총 이동거리: {total_distance}")

if total_distance == CANDIDATE:
    print("\nVERIFY_PASS")
else:
    print(f"\nVERIFY_FAIL (기댓값: {CANDIDATE}, 계산값: {total_distance})")