from sympy import *

a_val = Rational(-3, 4)
p = symbols('p', real=True)

# Condition AF1 = AF2: f(p) = p-1, i.e., (p+a)^2 = p-1
eq = (p + a_val)**2 - (p - 1)
solutions = solve(eq, p)
valid = [s for s in solutions if s >= 1]

if len(valid) != 1:
    print('VERIFY_FAIL: not exactly one p>=1')
else:
    pv = valid[0]
    f_p = (pv + a_val)**2

    # Find Q1 intersection of C1 and C2
    y = symbols('y', real=True)
    # C1: x = y^2/4, substitute into C2
    eq2 = (y - 3)**2 - 4*pv*(y**2/4 - f_p)
    ys = solve(eq2, y)
    pos_y = [s for s in ys if s > 0]

    if len(pos_y) != 1:
        print('VERIFY_FAIL: Q1 intersection not unique')
    else:
        yA = pos_y[0]
        xA = yA**2 / 4

        # Focal distances using focal property
        AF1 = xA + 1                  # C1: y^2=4x, directrix x=-1
        AF2 = xA - f_p + pv           # C2: directrix x=f(p)-p
        diff = simplify(AF1 - AF2)

        if diff == 0:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL: AF1 != AF2, diff =', diff)
