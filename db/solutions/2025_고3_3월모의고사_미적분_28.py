import sympy as sp

a = 3*sp.sqrt(3)
b = -a
x = sp.Symbol('x')
f = a*x**3 + b*x

# 1. f(-1) = 0 확인
assert f.subs(x, -1) == 0, 'f(-1) != 0'

# 2. 극댓값 = 2 확인
cp = sp.solve(sp.diff(f, x), x)
inner_cp = [c for c in cp if c.is_real and -1 < float(c.evalf()) < 1]
max_val = max(f.subs(x, c).evalf() for c in inner_cp)
assert abs(float(max_val) - 2) < 1e-10, f'local max = {max_val}'

# 3. g(-1/2) * g(2) 계산
g_minus_half = f.subs(x, sp.Rational(-1, 2))  # |x| < 1
g_two = 2 * sp.Integer(2)**2  # |x| > 1
product = sp.simplify(g_minus_half * g_two)

if sp.simplify(product - 9*sp.sqrt(3)) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {product}')
