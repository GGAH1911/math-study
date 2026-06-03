import sympy as sp

a = 2
m = sp.Rational(5, 2)

def g(v):
    return v**2 + 2

P = (g(a), a)
Q = (a, g(a))
O = (0, 0)
C = (m, m)

R_CO = sp.sqrt((C[0]-O[0])**2 + (C[1]-O[1])**2)
R_CP = sp.sqrt((C[0]-P[0])**2 + (C[1]-P[1])**2)
R_CQ = sp.sqrt((C[0]-Q[0])**2 + (C[1]-Q[1])**2)

area = sp.pi * R_CO**2

# P on f(x)=sqrt(x-2)
f_check = sp.sqrt(P[0] - 2) - P[1]

# Q on f_inv(x)=x^2+2
finv_check = Q[0]**2 + 2 - Q[1]

# slope of PQ = -1
slope_PQ = sp.Rational(Q[1]-P[1], Q[0]-P[0])

answer = m + g(a)

passed = (
    sp.simplify(R_CO - R_CP) == 0 and
    sp.simplify(R_CO - R_CQ) == 0 and
    sp.simplify(area - sp.Rational(25, 2)*sp.pi) == 0 and
    slope_PQ == -1 and
    f_check == 0 and
    finv_check == 0 and
    answer == sp.Rational(17, 2)
)

print('VERIFY_PASS' if passed else 'VERIFY_FAIL')
