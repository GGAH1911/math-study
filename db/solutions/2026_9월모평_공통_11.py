import sympy as sp
from sympy import symbols, integrate, Abs, simplify

t = symbols('t', real=True)
v = 3*t**2 - 10*t + 7

# 위치 함수
s = integrate(v, (t, 0, t))

# ㄱ 검증: t=1에서 v=0
v_at_1 = v.subs(t, 1)
print(f'v(1) = {v_at_1}')  # 0이어야 함

# ㄴ 검증: s(1) = 3
s_at_1 = s.subs(t, 1)
print(f's(1) = {s_at_1}')  # 3이어야 함

# ㄷ 검증: t=0~2 거리 = 4
# t=1과 7/3에서 부호 변화
s_at_0 = 0
s_at_2 = s.subs(t, 2)
distance_0_to_1 = abs(float(s_at_1) - float(s_at_0))
distance_1_to_2 = abs(float(s_at_2) - float(s_at_1))
total_distance = distance_0_to_1 + distance_1_to_2

print(f's(2) = {s_at_2}')  # 2
print(f'거리[0,1] = {distance_0_to_1}, 거리[1,2] = {distance_1_to_2}')
print(f'총 거리 = {total_distance}')  # 4이어야 함

if v_at_1 == 0 and s_at_1 == 3 and total_distance == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')