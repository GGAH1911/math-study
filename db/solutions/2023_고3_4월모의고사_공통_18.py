from sympy import symbols, limit, oo

x = symbols('x')

# 구한 함수
f_x = 2*x**2 + 5*x + 1

# 검증 1: f(0) = 1
f_0 = f_x.subs(x, 0)
assert f_0 == 1, f'f(0) = {f_0}, expected 1'

# 검증 2: 극한 조건
limit_expr = (x*f_x - 2*x**3 + 1) / x**2
limit_val = limit(limit_expr, x, oo)
assert limit_val == 5, f'Limit = {limit_val}, expected 5'

# 검증 3: f(1) 계산
f_1 = f_x.subs(x, 1)
assert f_1 == 8, f'f(1) = {f_1}, expected 8'

print('VERIFY_PASS')