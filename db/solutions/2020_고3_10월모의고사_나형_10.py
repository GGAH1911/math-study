from sympy import symbols, integrate, simplify

a, x = symbols('a x', positive=True, real=True)

# 두 곡선
line = a * x
parabola = x**2

# 교점 구하기
from sympy import solve
intersection_points = solve(line - parabola, x)
print(f'교점: {intersection_points}')

# 넓이 계산 (0부터 a까지)
integrand = line - parabola
area = integrate(integrand, (x, 0, a))
area_simplified = simplify(area)
print(f'넓이: {area_simplified}')

# a^3/6과 비교
from sympy import Rational
expected = a**3 / 6
if simplify(area_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')