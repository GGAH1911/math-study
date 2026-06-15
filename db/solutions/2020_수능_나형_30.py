CANDIDATE = 51

from sympy import symbols, Rational, diff, roots

try:
    x = symbols('x')
    f = Rational(32, 9)*x**3 + Rational(-16, 3)*x**2 + x
    
    assert f.subs(x, 0) == 0
    assert diff(f, x).subs(x, 1) == 1
    assert len(roots(f - x, x)) == 2
    assert len(roots(f + x, x)) == 2
    assert f.subs(x, 3) == CANDIDATE
    
    print("VERIFY_PASS")
except:
    print("VERIFY_FAIL")