import sympy as sp

x = sp.symbols('x', positive=True)
# 원래 함수
f = lambda u: 2**(1/sp.log(u, 2))

# 원래 방정식 8 f(f(x)) = f(x^2)
lhs = 8 * f(f(x))
rhs = f(x**2)
sols = sp.solve(sp.Eq(lhs, rhs), x)
# x>0, x!=1 만
sols = [s for s in sols if s.is_real and s > 0 and s != 1]
prod = sp.simplify(sp.prod(sols))

# p=3, q=prod, g(x)=log_2 x, g(4)=2
p = 3
q = prod
g4 = sp.log(4, 2)
val = sp.nsimplify(p * q * g4)

if sp.simplify(val - sp.Rational(3,4)) == 0 and sp.simplify(q - sp.Rational(1,8)) == 0:
    print('VERIFY_PASS')
else:
    # 수치 백업
    import math
    # 2t^2+6t-1=0 두 근
    t1 = (-6 + math.sqrt(44))/4
    t2 = (-6 - math.sqrt(44))/4
    x1, x2 = 2**t1, 2**t2
    # 원식 직접 검증
    def F(u):
        return 2**(1/math.log2(u))
    ok = True
    for xv in (x1, x2):
        if not math.isclose(8*F(F(xv)), F(xv*xv), rel_tol=1e-9):
            ok = False
    prod_n = x1*x2
    final = 3 * prod_n * math.log2(4)
    if ok and math.isclose(prod_n, 1/8, rel_tol=1e-9) and math.isclose(final, 0.75, rel_tol=1e-9):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
