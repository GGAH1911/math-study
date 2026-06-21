from sympy import symbols, Eq, solve, Rational, nsimplify
from sympy.stats import Normal, P

# table values P(0<=Z<=z)
table = {0.5: 0.1915, 1.0: 0.3413, 1.5: 0.4332, 2.0: 0.4772}

mu = 104
sigma = 4
n = 4
se = sigma / (n ** 0.5)  # standard error of sample mean = 2

# Build P(a <= Xbar <= 106) using the given table (table-consistent computation)
# For a candidate a, z_low=(a-104)/se, z_high=(106-104)/se=1.0
z_high = (106 - mu) / se  # 1.0

def prob_0_to_z(z):
    # use table by absolute value
    return table[abs(round(z, 1))]

def prob_between(zl, zh):
    # P(zl<=Z<=zh) with zl<=zh
    def signed(z):
        # returns P(0<=Z<=z) with sign by side: P(zl<=Z<=0)=P(0<=Z<=|zl|)
        return prob_0_to_z(z)
    if zl < 0 and zh >= 0:
        return prob_0_to_z(zl) + prob_0_to_z(zh)
    elif zl >= 0 and zh >= 0:
        return prob_0_to_z(zh) - prob_0_to_z(zl)
    else:
        return prob_0_to_z(zl) - prob_0_to_z(zh)

# Find integer a among options that yields 0.5328
target = 0.5328
found = None
for a in [99, 100, 101, 102, 103]:
    zl = (a - mu) / se
    try:
        val = prob_between(zl, z_high)
    except KeyError:
        continue
    if abs(val - target) < 1e-9:
        found = a
        break

# Cross-check with continuous normal CDF of sample mean
Xbar = Normal('Xbar', mu, se)
if found is not None:
    approx = float(P((Xbar >= found) & (Xbar <= 106)))
    # continuous value should be close to table-based 0.5328
    if found == 103 and abs(approx - 0.5328) < 0.01:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')
