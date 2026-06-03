import sympy as sp
try:
    a = 4*sp.sqrt(2)
    b = sp.Integer(6)
    x = sp.symbols('x', real=True)
    f = a*sp.sin(sp.pi*x/b) + 1
    # 원래 방정식 f(x)=5의 해를 [0, 5b/2]에서 모두 찾기
    # sin(pi x/6) = 4/a = 1/sqrt(2) ⇒ pi x/6 = pi/4+2k pi 또는 3pi/4+2k pi
    candidates = []
    for k in range(-3, 6):
        candidates.append(sp.Rational(3,2) + 12*k)
        candidates.append(sp.Rational(9,2) + 12*k)
    upper = sp.Rational(5,2)*b
    domain_xs = sorted([c for c in candidates if (c >= 0) and (c <= upper)])
    assert len(domain_xs) == 3, domain_xs
    xA, xB, xC = domain_xs
    # 각 해가 원식을 만족하는지
    for xi in domain_xs:
        assert sp.simplify(f.subs(x, xi) - 5) == 0
    # 조건: BC = AB + 6
    AB = xB - xA
    BC = xC - xB
    assert sp.simplify(BC - AB - 6) == 0
    # 조건: 삼각형 AOB 넓이 = 15/2 (O=(0,0), A=(xA,5), B=(xB,5))
    area = sp.Rational(1,2) * abs(xA*5 - xB*5)
    assert sp.simplify(area - sp.Rational(15,2)) == 0
    # 제약: a>4, b>0
    assert a > 4 and b > 0
    # 답: a^2 + b^2
    val = sp.simplify(a**2 + b**2)
    assert val == 68
    print('VERIFY_PASS')
except Exception:
    print('VERIFY_FAIL')
