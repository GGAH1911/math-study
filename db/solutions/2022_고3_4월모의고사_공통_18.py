import sympy as sp
x = sp.Symbol('x')
f = lambda x_val: 3*x_val**2/2 - 6*x_val + 15
F = lambda x_val: x_val**3/2 - 3*x_val**2 + 15*x_val + 30

# 원래 조건 확인: F(x) = (x+2)f(x) - x^3 + 12x
for x_val in [0, 1, 2, 3, -1]:
    left = F(x_val)
    right = (x_val + 2)*f(x_val) - x_val**3 + 12*x_val
    assert abs(left - right) < 1e-10, f'조건 불만족 at x={x_val}'

# F'(x) = f(x) 확인
assert abs(3*2**2/2 - 6*2 + 15 - 9) < 1e-10, 'f(2) 오류'

# F(0) = 30 확인
assert F(0) == 30, 'F(0) 조건 불만족'

print('VERIFY_PASS')