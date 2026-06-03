from sympy import *
a, b, c = -2, 2, 2
f = lambda x: a*x**3 + b*x**2 + c*x
f_prime = lambda x: 3*a*x**2 + 2*b*x + c

# 조건 검증
assert f(0) == 0, '조건 1: f(0)=0'
assert a + b + c == 2, '조건 2: f(1)=2'

# 점 (0,0)에서의 접선
slope1 = f_prime(0)
assert slope1 == c, '접선 기울기 c'
tangent1_y = lambda x: slope1 * x

# 점 (1,2)가 y=xf(x) 위에 있는지
assert 1 * f(1) == 2, '점 (1,2) 확인'

# 점 (1,2)에서의 접선
xf_x = lambda x: x * f(x)
xf_prime = lambda x: f(x) + x * f_prime(x)
slope2 = xf_prime(1)
tangent2_y = lambda x: 2 + slope2 * (x - 1)

# 두 접선이 일치하는지
assert slope1 == slope2, f'기울기 일치: {slope1} == {slope2}'
assert tangent1_y(1) == tangent2_y(1), '점 (1,2)에서 일치'
assert tangent1_y(0) == tangent2_y(0), '원점에서 일치'

result = f_prime(2)
assert result == -14, f'f\'(2) = {result}'
print('VERIFY_PASS')