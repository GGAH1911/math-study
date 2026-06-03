import sympy as sp
n = sp.symbols('n', positive=True, integer=True)
a_val, b_val = 1, 3
ok = True
for k in [1, 2]:
    a_n = sp.Rational(k, 2)**n
    expr = (a_val*a_n + sp.Rational(1,2)**n) / (a_n + b_val*sp.Rational(1,2)**n)
    lim = sp.limit(expr, n, sp.oo)
    if sp.simplify(lim - sp.Rational(k, 2)) != 0:
        ok = False
# k>=3 인 경우 발산해서 수렴 조건 위배 → k=1,2만 검사 대상
print('VERIFY_PASS' if ok and (a_val + b_val == 4) else 'VERIFY_FAIL')