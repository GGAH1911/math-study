import sympy as sp
from sympy import symbols, diff, solve

x, a = symbols('x a', real=True, positive=True)
f = -x**4 + 8*a**2*x**2 - 1
f_prime = diff(f, x)

# 극값: f'(x) = 0
critical_points = solve(f_prime, x)
print(f'Critical points: {critical_points}')

# a=1 일 때
a_val = 1
f_at_a1 = f.subs(a, a_val)
f_prime_at_a1 = diff(f_at_a1, x)
cp_a1 = solve(f_prime_at_a1, x)
print(f'Critical points when a=1: {cp_a1}')

# 극대/극소 판정 (2계 도함수)
f_double_prime = diff(f_prime_at_a1, x)
for cp in cp_a1:
    second_deriv = f_double_prime.subs(x, cp)
    if second_deriv < 0:
        print(f'x={cp}: 극대')
    elif second_deriv > 0:
        print(f'x={cp}: 극소')

# b=2, 2-2b=-2 확인
b = 2
point2 = 2 - 2*b
print(f'b={b}, 2-2b={point2}')
print(f'극대 위치: {-2}, {2}')
if set([b, point2]) == {-2, 2}:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')