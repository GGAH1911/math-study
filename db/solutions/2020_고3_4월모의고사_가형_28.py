CANDIDATE = 75

import sympy as sp

# a = 2^(sqrt(2)/2)
a = 2 ** (sp.sqrt(2)/2)
k = sp.Rational(1,1) / sp.sqrt(2)

# 조건 검증: OC = CA = AB
OC = k
CA = a**(-k)
AB = a**k - a**(-k)

tol = 1e-12
check1 = abs(float(OC - CA)) < tol
check2 = abs(float(CA - AB)) < tol

# y = 2*sqrt(2) 교점
x1 = a**(-2*sp.sqrt(2))
x2 = a**(2*sp.sqrt(2))

d = float(x2 - x1)
twenty_d = round(20 * d)

if check1 and check2 and twenty_d == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: OC==CA={check1}, CA==AB={check2}, 20d={twenty_d}, CANDIDATE={CANDIDATE}')
