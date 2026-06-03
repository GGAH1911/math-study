import sympy as sp
x = sp.Symbol('x')
# 원래 방정식
f = x**3 + 2*x - 3
# 근을 구함
roots = sp.solve(f, x)
# 허근 찾기
complex_roots = [r for r in roots if sp.im(r) != 0]
if complex_roots:
    root = complex_roots[0]
    a = sp.re(root)
    b = sp.im(root)
    a2b2 = a**2 * b**2
    a2b2_simplified = sp.simplify(a2b2)
    # 원래 방정식에 대입하여 검증
    check = f.subs(x, root)
    check_simplified = sp.simplify(check)
    if check_simplified == 0 and sp.simplify(a2b2_simplified - sp.Rational(11, 16)) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')