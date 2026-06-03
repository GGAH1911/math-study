from sympy import *
c_val = 2
F = (c_val, 0)
Fp = (-c_val, 0)
A = (3, 0)
P = (Rational(c_val+3,2), sqrt(55)*Rational(3-c_val,6))
PF = sqrt((P[0]-F[0])**2+(P[1]-F[1])**2)
PFp = sqrt((P[0]-Fp[0])**2+(P[1]-Fp[1])**2)
PA = sqrt((P[0]-A[0])**2+(P[1]-A[1])**2)
FA = sqrt((A[0]-F[0])**2+(A[1]-F[1])**2)
# 타원 조건 검증
cond1 = Eq(simplify(PF+PFp), 6)
cond2 = Eq(simplify(PA+PFp), 6)
# cos(AFP) 검증
FA_v = (A[0]-F[0], A[1]-F[1])
FP_v = (P[0]-F[0], P[1]-F[1])
dot = FA_v[0]*FP_v[0]+FA_v[1]*FP_v[1]
cos_afp = simplify(dot/(sqrt(FA_v[0]**2+FA_v[1]**2)*sqrt(FP_v[0]**2+FP_v[1]**2)))
cond3 = Eq(cos_afp, Rational(3,8))
# 둘레 검증
peri = simplify(PF+PA+FA)
cond4 = Eq(peri, Rational(11,3))
if all([cond1, cond2, cond3, cond4]):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', cond1, cond2, cond3, cond4)