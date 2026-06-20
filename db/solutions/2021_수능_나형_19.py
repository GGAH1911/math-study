import math

def Phi(x, mu=0.0, sigma=1.0):
    return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))

# X ~ N(8, 3^2)
P_X = Phi(8, 8, 3) - Phi(4, 8, 3)  # P(4<=X<=8)

# Y ~ N(m, sigma^2): pick arbitrary positive sigma, solve m from the condition
sigma = 3.0

def cond(m):
    # P(4<=X<=8) + P(Y>=8) - 1/2
    P_Y_ge8 = 1 - Phi(8, m, sigma)
    return P_X + P_Y_ge8 - 0.5

# bisection for m on [-100,100] (cond increases in m)
lo, hi = -100.0, 100.0
for _ in range(300):
    mid = (lo + hi) / 2
    if cond(lo) * cond(mid) <= 0:
        hi = mid
    else:
        lo = mid
m = (lo + hi) / 2

# target probability P(Y <= 8 + 2*sigma/3)
target = Phi(8 + 2*sigma/3, m, sigma)

CANDIDATE = 0.9772  # = 0.5 + 0.4772 (table z=2.0)
if abs(target - CANDIDATE) < 1e-3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
