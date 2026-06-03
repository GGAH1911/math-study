import sympy as sp

a = 4 - 2*sp.sqrt(2)
b = 3 - 2*sp.sqrt(2)
x = sp.Symbol('x', real=True)

# b > 0 체크
assert sp.simplify(b).evalf() > 0

# 원 함수 정의 (이미지의 piecewise)
def f_val(xv):
    if xv <= 0:
        return xv**2 + a*xv + b
    else:
        return -xv**2 + a*xv - b

# (나) 조건: f(k)*f(k+1) >= 0 모든 정수 k에 대해 확인
for k in range(-15, 16):
    p = sp.simplify(f_val(k) * f_val(k+1))
    if p.evalf() < -1e-9:
        print('VERIFY_FAIL')
        raise SystemExit

# (가) 조건: N(t)=2 인 t가 정확히 1개여야 함
# 이론적으로 a^2 = 8b 이면 그러한 유일한 t는 -b
assert sp.simplify(a**2 - 8*b) == 0

def count_distinct(t_val):
    left_roots = sp.solve(x**2 + a*x + b - t_val, x)
    right_roots = sp.solve(-x**2 + a*x - b - t_val, x)
    roots = set()
    for r in left_roots:
        if r.is_real and sp.simplify(r).evalf() <= 1e-12:
            roots.add(round(float(sp.simplify(r).evalf()), 10))
    for r in right_roots:
        if r.is_real and sp.simplify(r).evalf() > 1e-12:
            roots.add(round(float(sp.simplify(r).evalf()), 10))
    return len(roots)

# t = -b 에서 정확히 2개
if count_distinct(-b) != 2:
    print('VERIFY_FAIL'); raise SystemExit
# t > -b 부근 (예: 0, b/2)에서는 4개 (≠2)
for tv in [sp.Integer(0), b/2, -b/2]:
    if count_distinct(tv) == 2:
        print('VERIFY_FAIL'); raise SystemExit
# t = b 에서 3개 (≠2)
if count_distinct(b) != 3:
    print('VERIFY_FAIL'); raise SystemExit
# t > b 에서 1개
if count_distinct(b + sp.Rational(1,10)) != 1:
    print('VERIFY_FAIL'); raise SystemExit
# t < -b 에서 1개
if count_distinct(-b - sp.Rational(1,10)) != 1:
    print('VERIFY_FAIL'); raise SystemExit

# f(2) 계산 및 p-q 확인
f2 = sp.simplify(f_val(2))
expected = 1 - 2*sp.sqrt(2)
if sp.simplify(f2 - expected) != 0:
    print('VERIFY_FAIL'); raise SystemExit

# p=1, q=-2 → p-q = 3
if 1 - (-2) != 3:
    print('VERIFY_FAIL'); raise SystemExit

print('VERIFY_PASS')
