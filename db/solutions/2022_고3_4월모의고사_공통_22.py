import sympy as sp
from sympy import symbols, diff, Rational, expand, factor, solve

x = symbols('x')
a = Rational(3, 2)

# f(x) 정의
f = x**3 - Rational(21, 2)*x**2 + 30*x - Rational(1, 2)

# 조건 1: f(0) = -1/2
assert f.subs(x, 0) == Rational(-1, 2), 'f(0) check failed'

# 조건 2: g'(x) = f'(x+a) * f'(x-a)의 근
f_prime = diff(f, x)
g_prime = f_prime.subs(x, x+a) * f_prime.subs(x, x-a)
g_prime_factored = factor(g_prime)

# g'(x)의 근과 중복도
roots_with_mult = sp.roots(g_prime, x)
extreme_points = [r for r, mult in roots_with_mult.items() if mult % 2 == 1]
extreme_points_sorted = sorted([float(r) for r in extreme_points])

# 극값이 1/2과 13/2에서만 존재하는지 확인
assert len(extreme_points) == 2, f'Expected 2 extreme points, got {len(extreme_points)}'
assert abs(extreme_points_sorted[0] - 0.5) < 1e-9, f'First extreme at {extreme_points_sorted[0]}'
assert abs(extreme_points_sorted[1] - 6.5) < 1e-9, f'Second extreme at {extreme_points_sorted[1]}'

# 최종 답
f_1 = f.subs(x, 1)
result = a * f_1
assert result == 30, f'a*f(1) = {result}'

print('VERIFY_PASS')