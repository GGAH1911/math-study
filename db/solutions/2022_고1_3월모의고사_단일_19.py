from sympy import *
s = 3 + 2*sqrt(2)
a = sqrt(s)/2
beta_cos = 1/(2*sqrt(s))
beta_sin_sq = (4*s - 1)/(4*s)

# AE = 2BC 확인
AE = s - 1
BC = 2*a
print('AE:', simplify(AE))
print('2*BC:', simplify(2*BC))
print('AE = 2BC?', simplify(AE - 2*BC) == 0)

# cos²β + sin²β = 1 확인
print('cos²β + sin²β:', simplify(1/(4*s) + beta_sin_sq))

if simplify(AE - 2*BC) == 0 and simplify(1/(4*s) + beta_sin_sq) == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')