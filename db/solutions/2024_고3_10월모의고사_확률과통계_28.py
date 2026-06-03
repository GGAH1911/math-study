import math

def Phi(z):
    return 0.5*(1+math.erf(z/math.sqrt(2)))

# Table values from the problem
table = {0.5:0.1915, 1.0:0.3413, 1.5:0.4332, 2.0:0.4772, 2.5:0.4938}

# Enumerate candidate (mu_X, mu_Y) satisfying (가), (나)
# Both N(mu,1); horizontal line y=k cuts each curve symmetrically about its mean.
# Set of x-coords of all intersections = {1,2,3,4}.
# So partition {1,2,3,4} into two pairs with equal half-width (same k, same sigma).
from itertools import permutations
cands = []
xs = [1,2,3,4]
# possible pair-partitions where both pairs have same half-width
partitions = [
    ([1,2],[3,4]),  # half=0.5 each
    ([1,3],[2,4]),  # half=1 each
    ([1,4],[2,3]),  # half=1.5,0.5 -> not equal, excluded
]
for A,B in partitions:
    mA = sum(A)/2
    mB = sum(B)/2
    hwA = (A[1]-A[0])/2
    hwB = (B[1]-B[0])/2
    if abs(hwA-hwB) > 1e-9:
        continue
    # check matching k via same density value: f_A(x)=f_B(x) automatically since same sigma=1 and same half-width
    for muX, muY in [(mA,mB),(mB,mA)]:
        diff = Phi(2-muX) - Phi(2-muY)
        if diff > 0.5:
            cands.append((muX,muY,diff))

assert len(cands)==1, cands
muX, muY, _ = cands[0]

# Compute P(X >= 2.5) using table-style values
z = (2.5 - muX)/1.0
# Use table 0.1915,0.3413,... For z=1.0, P(0<=Z<=z)=0.3413, so P(Z>=1)=0.5-0.3413=0.1587
z_round = round(z,1)
prob = 0.5 - table[z_round]

ans = 0.1587
if abs(prob - ans) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', prob)
