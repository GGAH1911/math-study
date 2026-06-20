from sympy import symbols, integrate, solve, Rational, simplify

t = symbols('t', real=True)
a_val = 3

# 속도 함수
v = t**2 - a_val*t

# 속도가 0인 시점 확인
velocity_zeros = solve(v, t)
print(f'Speed zero at: {velocity_zeros}')

# 0에서 a까지 구간에서 속도는 음수이므로 |v(t)| = -(t^2 - at) = at - t^2
# 따라서 거리 = ∫₀ᵃ (at - t²) dt
distance_integral = integrate(a_val*t - t**2, (t, 0, a_val))
expected_distance = Rational(9, 2)

print(f'Distance traveled: {distance_integral}')
print(f'Expected distance: {expected_distance}')
print(f'Match: {distance_integral == expected_distance}')

if distance_integral == expected_distance:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')