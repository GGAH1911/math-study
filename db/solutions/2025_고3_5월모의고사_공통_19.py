import sympy as sp

f = lambda x: x**3 - x**2 - x + 1
f_prime = lambda x: 3*x**2 - 2*x - 1

# 조건 1: f(0) = 1
assert f(0) == 1, 'f(0) != 1'

# 조건 2: f(1) = 0
assert f(1) == 0, 'f(1) != 0'

# 조건 3: 점 (0,1)에서의 접선이 점 (1,0)을 지남
slope = f_prime(0)
assert slope * 1 + 1 == 0, 'tangent does not pass (1,0)'

# 조건 4: 접선과 곡선의 교점 확인
x = sp.Symbol('x')
intersection_eq = x**3 - x**2 - x + 1 - (slope * x + 1)
roots = sp.solve(intersection_eq, x)
assert 0 in roots and 1 in roots, 'intersection points incorrect'

# f(3) 계산 및 검증
answer = f(3)
if answer == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')