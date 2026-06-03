import sympy as sp

x = sp.Symbol('x', real=True)
k = sp.Rational(14, 3)
f1 = x**3 + x**2         # 원 문제의 첫 번째 곡선
f2 = -x**2 + k           # 원 문제의 두 번째 곡선

# 0 < x < 2 에서 두 곡선의 교점 alpha 를 수치적으로 구함
poly = sp.Poly(f1 - f2, x)
roots = sp.nroots(poly.as_expr(), n=30)
alpha = None
for r in roots:
    cr = complex(r)
    if abs(cr.imag) < 1e-12 and 0 < cr.real < 2:
        alpha = sp.Float(cr.real, 30)
        break
if alpha is None:
    print('VERIFY_FAIL'); raise SystemExit

# 그림에 따라: 0..alpha 에서 f2 >= f1 (영역 A), alpha..2 에서 f1 >= f2 (영역 B)
A = sp.integrate(f2 - f1, (x, 0, alpha))
B = sp.integrate(f1 - f2, (x, alpha, 2))

# A, B 가 모두 양수이고 같은지 확인
ok_sign = float(A) > 0 and float(B) > 0
ok_eq = abs(float(A - B)) < 1e-9
ok_k = 4 < float(k) < 5

if ok_sign and ok_eq and ok_k:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
