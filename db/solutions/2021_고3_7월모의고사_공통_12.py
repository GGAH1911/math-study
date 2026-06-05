import numpy as np
from sympy import symbols, limit, oo, expand, simplify

x = symbols('x')

# 정의된 f(x)
f = 2*(x-3)**2

# 극한 조건 검증
limit_check = limit(f / (x**2 - 3*x - 5), x, oo)
print(f'Limit check (should be 2): {limit_check}')
assert limit_check == 2, 'VERIFY_FAIL'

# f(3) = 0 확인
f_at_3 = f.subs(x, 3)
print(f'f(3) = {f_at_3} (should be 0)')
assert f_at_3 == 0, 'VERIFY_FAIL'

# f(1) 계산
f_at_1 = f.subs(x, 1)
print(f'f(1) = {f_at_1}')
assert f_at_1 == 8, 'VERIFY_FAIL'

print('VERIFY_PASS')