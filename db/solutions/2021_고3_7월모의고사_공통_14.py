from sympy import symbols, integrate, solve, Abs
t = symbols('t', real=True, positive=True)
v = 3*t**2 - 6*t
x = integrate(v, t)  # x(t) = t^3 - 3*t^2
a = 6*t - 6

# 가: t=2에서 방향 바뀌는가
v_at_2_minus = v.subs(t, 1.999)
v_at_2_plus = v.subs(t, 2.001)
print(f'v(1.999)={float(v_at_2_minus):.4f}, v(2.001)={float(v_at_2_plus):.4f}')
assert float(v_at_2_minus) < 0 and float(v_at_2_plus) > 0

# 나: x(2) = -4
x_2 = x.subs(t, 2)
assert x_2 == -4
print(f'x(2) = {x_2}')

# 다: t=0부터 a=12까지 거리 = 8
t_accel = solve(a - 12, t)[0]
print(f't when a=12: {t_accel}')
assert t_accel == 3

x_0 = 0
x_2_val = -4
x_3 = x.subs(t, 3)
dist = abs(x_2_val - x_0) + abs(float(x_3) - x_2_val)
print(f'x(0)={x_0}, x(2)={x_2_val}, x(3)={x_3}')
print(f'distance = {dist}')
assert dist == 8

print('VERIFY_PASS')