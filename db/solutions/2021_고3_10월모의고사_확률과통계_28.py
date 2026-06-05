from fractions import Fraction

# Brute-force enumeration over all functions f: X->X satisfying conditions
# X = {1,...,8}, conditions: f(2n-1) < f(2n) for n=1,2,3,4

total = 0
favorable = 0

X = range(1, 9)

for f1 in X:
    for f2 in X:
        if not (f1 < f2): continue
        for f3 in X:
            for f4 in X:
                if not (f3 < f4): continue
                for f5 in X:
                    for f6 in X:
                        if not (f5 < f6): continue
                        for f7 in X:
                            for f8 in X:
                                if not (f7 < f8): continue
                                total += 1
                                if f1 == f5:
                                    favorable += 1

prob = Fraction(favorable, total)
expected = Fraction(5, 28)
if prob == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {prob}, expected {expected}')
