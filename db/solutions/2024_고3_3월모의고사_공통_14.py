from fractions import Fraction

def L(a,b,t):
    # x<=0 와 (x-a)^2 = t+3a^2/4 - b^2
    disc = t + Fraction(3*a*a,4) - b*b
    if disc < 0: return 0
    if disc == 0:
        return 1 if a <= 0 else 0
    a_sq = Fraction(a*a)
    c1 = (a <= 0) and (disc <= a_sq)   # x = a + sqrt(disc) <= 0
    c2 = (a <= 0) or (disc >= a_sq)    # x = a - sqrt(disc) <= 0
    return int(c1)+int(c2)

def R(t):
    if t < 1: return 0
    if t == 1: return 1
    if t < 5: return 2
    if t == 5: return 1
    return 1

def g(a,b,t): return L(a,b,t)+R(t)

def ndisc(a,b):
    cands = {Fraction(1), Fraction(5), Fraction(a*a,4)+b*b}
    if a < 0:
        cands.add(-Fraction(3*a*a,4)+b*b)
    eps = Fraction(1, 10**9)
    n = 0
    for k in cands:
        gl = g(a,b,k-eps); gk = g(a,b,k); gr = g(a,b,k+eps)
        if gl != gk or gk != gr:
            n += 1
    return n

pairs = []
for a in range(-15,16):
    for b in range(-15,16):
        if ndisc(a,b) == 2:
            pairs.append((a,b))

print('pairs:', sorted(pairs))
print('count:', len(pairs))
print('VERIFY_PASS' if len(pairs)==5 else 'VERIFY_FAIL')
