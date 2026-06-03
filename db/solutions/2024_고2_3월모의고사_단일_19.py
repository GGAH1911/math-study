import sympy as sp

# Answer to verify
a_val = sp.Rational(34, 9)
b_val = sp.Rational(-4, 3)
answer = a_val + b_val

# Setup from original problem
Ax, Ay = sp.Rational(0), sp.Rational(6)
Bx, By = sp.Rational(9), sp.Rational(0)
# P = 2:1 internal division of AB
Px = (2*Bx + 1*Ax) / sp.Rational(3)
Py = (2*By + 1*Ay) / sp.Rational(3)

# Original circle eq: x^2 + y^2 - 2a x - 2b y = 0
x, y = sp.symbols('x y', real=True)
circle = x**2 + y**2 - 2*a_val*x - 2*b_val*y

# Check 1: P lies on the circle
val_P = sp.simplify(circle.subs({x: Px, y: Py}))
if val_P != 0:
    print('VERIFY_FAIL')
else:
    # Check 2: Line AB meets circle ONLY at P.
    # Parametrize line AB through A and B.
    t = sp.Symbol('t', real=True)
    Lx = Ax + t*(Bx - Ax)
    Ly = Ay + t*(By - Ay)
    expr = sp.expand(circle.subs({x: Lx, y: Ly}))
    roots = sp.solve(expr, t)
    # Need exactly one distinct root corresponding to point P
    distinct = set(sp.simplify(r) for r in roots)
    # t for P: Lx=Px -> 0 + 9t = 6 -> t = 2/3
    if len(distinct) == 1 and sp.simplify(list(distinct)[0] - sp.Rational(2,3)) == 0:
        # Confirm sum matches the multiple choice value 22/9
        if sp.simplify(answer - sp.Rational(22, 9)) == 0:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')
