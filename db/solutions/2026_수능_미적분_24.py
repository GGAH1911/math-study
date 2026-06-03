import sympy as sp
x = sp.symbols('x')
f = sp.sqrt(sp.sin(x) - sp.sin(x)**3)
val = sp.integrate(f, (x, 0, sp.pi/2))
val_simplified = sp.simplify(val)
answer = sp.Rational(2, 3)
if sp.simplify(val_simplified - answer) == 0:
    print('VERIFY_PASS')
else:
    # fallback numeric check
    import math
    from sympy import N
    diff = float(N(val_simplified)) - float(answer)
    if abs(diff) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
