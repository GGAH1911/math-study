from math import erf, sqrt

def Phi(x):
    return 0.5*(1+erf(x/sqrt(2)))

def P_normal(a, b, mu, sigma):
    return Phi((b-mu)/sigma) - Phi((a-mu)/sigma)

k = 20.25
pA = P_normal(8.9, 9.4, 9, 0.4)
pB = P_normal(19, k, 20, 1)

if abs(pA - pB) < 1e-12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', pA, pB)