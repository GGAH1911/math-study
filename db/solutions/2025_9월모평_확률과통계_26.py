from math import erf, sqrt
def Phi(z):
    return 0.5*(1+erf(z/sqrt(2)))
m = 8
# X-bar ~ N(m, 6^2/9) -> sd = 2
sd_X = 6/sqrt(9)
P1 = Phi((12 - m)/sd_X)
# Y-bar ~ N(6, 2^2/4) -> sd = 1
sd_Y = 2/sqrt(4)
P2 = 1 - Phi((8 - 6)/sd_Y)
total = P1 + P2
print('VERIFY_PASS' if abs(total - 1) < 1e-9 else 'VERIFY_FAIL')