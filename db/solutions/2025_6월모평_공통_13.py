import sympy as sp

x = sp.symbols('x', real=True)
m_val = sp.Rational(-4, 3)
f = sp.Rational(1,4)*x**3 + sp.Rational(1,2)*x
g = m_val*x + 2

# m < -1 조건 확인
assert m_val < -1

# 원래 방정식 f(x) = g(x) 의 0과 2 사이 근 alpha 수치적으로
poly = sp.Poly(f - g, x)
roots = poly.nroots(n=30)
alpha = None
for r in roots:
    if abs(sp.im(r)) < 1e-12:
        rv = float(sp.re(r))
        if 0 < rv < 2:
            alpha = sp.re(r)
            break

if alpha is None:
    print('VERIFY_FAIL')
else:
    # 그림대로: A 는 [0, alpha] 에서 직선 - 곡선, B 는 [alpha, 2] 에서 곡선 - 직선
    A = sp.integrate(g - f, (x, 0, alpha))
    B = sp.integrate(f - g, (x, alpha, 2))
    diff = sp.N(B - A, 30)
    target = sp.Rational(2, 3)
    if abs(diff - target) < sp.Rational(1, 10**12):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
