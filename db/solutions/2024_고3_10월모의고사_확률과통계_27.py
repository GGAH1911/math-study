from fractions import Fraction
from math import comb

found = None
for a in range(0,8):
    for b in range(0,8):
        for c in range(0,8):
            if a+b+c != 7: continue
            total = comb(7,2)
            # P(X=4) requires picking two 2's
            p4 = Fraction(comb(b,2), total)
            p2 = Fraction(a*b, total)
            p6 = Fraction(b*c, total)
            if p4 == Fraction(1,21) and 2*p2 == 3*p6:
                p1 = Fraction(comb(a,2), total)
                p3 = Fraction(a*c, total)
                p_le3 = p1 + p2 + p3
                found = (a,b,c,p_le3)
if found is None:
    print('VERIFY_FAIL')
else:
    a,b,c,p_le3 = found
    if p_le3 == Fraction(5,7):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
