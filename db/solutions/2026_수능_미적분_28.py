import sympy as sp

s = sp.Symbol('s', positive=True)

# 원래 함수 조건 확인: t = s^3/(1+s)
t_func = s**3 / (1 + s)

# 경계값 확인
t_at_1 = t_func.subs(s, 1)
t_at_3 = t_func.subs(s, 3)
assert t_at_1 == sp.Rational(1,2), f'boundary s=1 failed: {t_at_1}'
assert t_at_3 == sp.Rational(27,4), f'boundary s=3 failed: {t_at_3}'

# 치환 적분: integral of s * dt/ds ds from 1 to 3
dt_ds = sp.diff(t_func, s)
integrand = s * dt_ds  # = s^3*(2s+3)/(1+s)^2

result = sp.integrate(integrand, (s, 1, 3))
expected = sp.Rational(157, 12) + sp.ln(2)

diff = sp.simplify(result - expected)
if diff == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: result={result}, expected={expected}, diff={diff}')
