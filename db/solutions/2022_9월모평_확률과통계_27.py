from math import sqrt
from statistics import NormalDist
N = NormalDist()
# Standard normal table given in problem
table = {0.5:0.1915, 1.0:0.3413, 1.5:0.4332, 2.0:0.4772}
# Choose any sigma>0, n>=1 satisfying sigma/sqrt(n)=5
for n in [1, 4, 9, 25]:
    sigma = 5*sqrt(n)
    # X-bar SD
    sd_X = sigma/sqrt(n)
    # Check P(Xbar<=215) approx 0.1587 using table-based value (Phi(-1)=0.5-0.3413=0.1587)
    z1 = (215-220)/sd_X
    p1_table = 0.5 - table[abs(z1)]
    assert abs(p1_table - 0.1587) < 1e-4, p1_table
    # Y-bar SD with sigma_Y = 1.5*sigma, sample size 9n
    sigma_Y = 1.5*sigma
    sd_Y = sigma_Y/sqrt(9*n)
    z2 = (235-240)/sd_Y
    # P(Ybar>=235) = P(Z>=z2) = 0.5 + table[|z2|] since z2<0
    assert z2 == -2.0, z2
    p2_table = 0.5 + table[abs(z2)]
    assert abs(p2_table - 0.9772) < 1e-6, p2_table
print('VERIFY_PASS')
