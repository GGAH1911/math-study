import sympy as sp

x = sp.Symbol('x', real=True)
my_k = 3
my_alpha = sp.Rational(4, 3) * sp.pi
my_product = my_k * my_alpha

# (1) alpha가 원래 방정식 2 sin^2 x - 3 cos x = k를 만족하는지
lhs = sp.simplify(2*sp.sin(my_alpha)**2 - 3*sp.cos(my_alpha))
if sp.simplify(lhs - my_k) != 0:
    print('VERIFY_FAIL')
else:
    # (2) [0, 2pi]에서 원래 방정식의 실근을 직접 모두 찾는다.
    t = sp.Symbol('t', real=True)
    # 2 sin^2 x - 3 cos x = k  =>  2(1-t^2) - 3t - k = 0
    poly = 2*(1 - t**2) - 3*t - my_k
    t_sols = sp.solve(poly, t)

    x_sols = []
    for ts in t_sols:
        tv = float(ts)
        if -1 - 1e-12 <= tv <= 1 + 1e-12:
            a = sp.acos(ts)
            x_sols.append(sp.simplify(a))
            if not (sp.simplify(ts - 1) == 0 or sp.simplify(ts + 1) == 0):
                x_sols.append(sp.simplify(2*sp.pi - a))

    # 중복 제거 + 정렬
    uniq = []
    for s in x_sols:
        if all(sp.simplify(s - u) != 0 for u in uniq):
            uniq.append(s)
    uniq.sort(key=lambda r: float(r))

    # 모두 원래 방정식에 만족하는지 한 번 더 확인
    ok = all(sp.simplify(2*sp.sin(s)**2 - 3*sp.cos(s) - my_k) == 0 for s in uniq)
    if not ok:
        print('VERIFY_FAIL')
    elif len(uniq) != 3:
        print('VERIFY_FAIL')
    elif sp.simplify(uniq[-1] - my_alpha) != 0:
        print('VERIFY_FAIL')
    elif sp.simplify(my_product - 4*sp.pi) != 0:
        print('VERIFY_FAIL')
    else:
        print('VERIFY_PASS')
