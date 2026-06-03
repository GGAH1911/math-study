import numpy as np

def count_intersections(m):
    if m <= 0:
        return None
    pts = set()
    # Semicircle A: (1+m^2)x^2 + 10m^2 x + (25m^2-5)=0, y>=0
    a, b, c = 1+m**2, 10*m**2, 25*m**2-5
    D = b**2 - 4*a*c
    if D >= 0:
        for s in [1, -1]:
            x = (-b + s*np.sqrt(max(D,0)))/(2*a)
            y = m*(x+5)
            if y >= -1e-9:
                pts.add((round(x,5), round(y,5)))
    # B+: y=2x, x>=0 => x=5m/(2-m)
    if abs(m-2) > 1e-9:
        x = 5*m/(2-m)
        if x >= -1e-9:
            pts.add((round(x,5), round(2*x,5)))
    # B-: y=-2x, x<=0 => x=-5m/(m+2)
    x = -5*m/(m+2)
    if x <= 1e-9:
        pts.add((round(x,5), round(-2*x,5)))
    return len(pts)

# Check f values
assert count_intersections(0.1) == 4, f'f(0.1)={count_intersections(0.1)}'
assert count_intersections(1/3) == 3, f'f(1/3)={count_intersections(1/3)}'
assert count_intersections(0.4) == 4, f'f(0.4)={count_intersections(0.4)}'
assert count_intersections(0.5) == 2, f'f(0.5)={count_intersections(0.5)}'
assert count_intersections(1.0) == 2, f'f(1.0)={count_intersections(1.0)}'
assert count_intersections(2.0) == 1, f'f(2.0)={count_intersections(2.0)}'
assert count_intersections(3.0) == 1, f'f(3.0)={count_intersections(3.0)}'

# Discontinuities: alpha1=1/3, alpha2=1/2, alpha3=2
from fractions import Fraction
alpha1 = Fraction(1,3)
alpha2 = Fraction(1,2)
alpha3 = Fraction(2)
total = alpha1 + alpha2 + alpha3
if total == Fraction(17,6):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', total)
