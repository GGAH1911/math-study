from sympy import Rational, Abs

O = (Rational(0), Rational(0))
A = (Rational(0), Rational(-5))
B = (Rational(3), Rational(-3))

def shoelace_area(pts):
    n = len(pts)
    s = sum(pts[i][0]*pts[(i+1)%n][1] - pts[(i+1)%n][0]*pts[i][1] for i in range(n))
    return Abs(s) / 2

def get_slope(P, Q):
    dx = Q[0] - P[0]
    if dx == 0:
        return None
    return (Q[1] - P[1]) / dx

def parallel(P1, P2, P3, P4):
    s1 = get_slope(P1, P2)
    s2 = get_slope(P3, P4)
    if s1 is None and s2 is None: return True
    if s1 is None or s2 is None: return False
    return s1 == s2

C_candidates = [(Rational(-2), Rational(-4,3)), (Rational(-2), Rational(-3))]

y_coords = []
all_ok = True
for C in C_candidates:
    cx, cy = C
    if not (cx < 0 and cy < 0):
        print('VERIFY_FAIL: not third quadrant'); all_ok = False; break
    if not (cy > -5):
        print('VERIFY_FAIL: y not > -5'); all_ok = False; break
    area = shoelace_area([O, C, A, B])
    if area != Rational(25, 2):
        print(f'VERIFY_FAIL: area={area}'); all_ok = False; break
    oc_ab = parallel(O, C, A, B)
    ca_bo = parallel(C, A, B, O)
    if not (oc_ab != ca_bo):
        print('VERIFY_FAIL: not trapezoid'); all_ok = False; break
    y_coords.append(cy)

if all_ok:
    product = y_coords[0] * y_coords[1]
    if product == 4:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: product={product}')
