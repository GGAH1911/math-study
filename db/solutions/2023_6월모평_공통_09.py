import sympy as sp
from sympy import symbols, solve, diff

x, a = symbols('x a', real=True)

# 원래 함수 정의
f = x**3 - x + 6
g = x**2 + a

# 조건: f(x) >= g(x) for all x >= 0
# 즉, x^3 - x + 6 >= x^2 + a
# x^3 - x^2 - x + 6 >= a

h = x**3 - x**2 - x + 6
h_prime = diff(h, x)
critical_pts = solve(h_prime, x)
print(f'Critical points: {critical_pts}')

# x >= 0에서의 임계점
valid_critical = [pt for pt in critical_pts if pt >= 0]
print(f'Valid critical points (x >= 0): {valid_critical}')

# 최솟값 계산
values = []
for pt in valid_critical:
    val = h.subs(x, pt)
    values.append(float(val))
    print(f'h({pt}) = {val}')

value_at_0 = h.subs(x, 0)
values.append(float(value_at_0))
print(f'h(0) = {value_at_0}')

min_value = min(values)
print(f'Minimum of h(x) for x >= 0: {min_value}')

# 검증: a = 5일 때 f(x) >= g(x) for all x >= 0
a_max = 5
g_test = x**2 + a_max
difference = f - g_test
print(f'\nVerification with a = {a_max}:')
print(f'f(x) - g(x) = {difference}')

# x >= 0에서 f(x) - g(x) >= 0인지 확인
min_diff = min_value - a_max
print(f'Minimum of f(x) - g(x) for x >= 0: {min_diff}')

if min_diff >= 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')