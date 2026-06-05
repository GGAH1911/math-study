import sympy as sp
x = sp.Symbol('x')
C = -1
f = x**2 + 4*x + C

# 조건 1: f'(x) = 2x + 4 확인
f_prime = sp.diff(f, x)
assert f_prime == 2*x + 4, 'f\'(x) 조건 불만족'

# 조건 2: f(-1) + f(1) = 0 확인
f_minus1 = f.subs(x, -1)
f_1 = f.subs(x, 1)
assert f_minus1 + f_1 == 0, 'f(-1) + f(1) 조건 불만족'

# 답 검증
f_2 = f.subs(x, 2)
assert f_2 == 11, f'f(2) = {f_2} != 11'
print('VERIFY_PASS')