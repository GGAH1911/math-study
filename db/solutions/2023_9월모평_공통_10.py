from sympy import symbols, integrate

t, a = symbols('t a')
v = 3*t**2 + a*t

# 위치 함수 (t=0에서 원점 출발)
x_P = integrate(v, (t, 0, t))  # t^3 + a/2 * t^2

# t=2에서 P의 위치
x_P_at_2 = x_P.subs(t, 2)  # 8 + 2a

# A의 위치 = 6, 거리 = 10, a = 4 대입
a_val = 4
pos_P = x_P_at_2.subs(a, a_val)  # 8 + 8 = 16
pos_A = 6
distance = abs(pos_P - pos_A)  # |16 - 6| = 10

if distance == 10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: distance={distance}, expected 10')
