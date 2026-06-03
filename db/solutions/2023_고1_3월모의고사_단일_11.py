from sympy import Rational, symbols, Eq, solve
d = symbols('d', positive=True, real=True)
# 전체 시간: d/3 + d/4 <= 2
time_eq = d/3 + d/4
# 등호일 때 d값
d_max = solve(Eq(time_eq, 2), d)[0]
print(f'd_max = {d_max}')
# 왕복 거리
total_distance = 2 * d_max
print(f'total_distance = {total_distance}')
# 검증
verify_time = d_max/3 + d_max/4
print(f'verify_time = {verify_time}')
if verify_time == 2 and total_distance == Rational(48, 7):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')