from sympy import *

k = symbols('k', positive=True, integer=True)

# 원래 문제: y = x^2 + 5x + 3, x = n
# P_n = (n, n^2+5n+3)
# 기울기 -1인 직선: y = -x + n^2+6n+3
# Q_n = (n^2+6n+3, 0), R_n = (0, n^2+6n+3)
# |P_nQ_n| = (n^2+5n+3)*sqrt(2)
# |P_nR_n| = n*sqrt(2)
# |P_nQ_n| - |P_nR_n| = (n^2+4n+3)*sqrt(2) = (n+1)(n+3)*sqrt(2)
# 일반항 = 3*sqrt(2) / ((n+1)(n+3)*sqrt(2)) = 3/((n+1)(n+3))

term = Rational(3,1) / ((k+1)*(k+3))
total = summation(term, (k, 1, oo))

expected = Rational(5, 4)

# 원래 식으로 부분검증 (n=1,2,3)
def check_term(n_val):
    Px, Py = n_val, n_val**2 + 5*n_val + 3
    Qx, Qy = n_val**2 + 6*n_val + 3, 0
    Rx, Ry = 0, n_val**2 + 6*n_val + 3
    PQ = sqrt((Qx-Px)**2 + (Qy-Py)**2)
    PR = sqrt((Rx-Px)**2 + (Ry-Py)**2)
    return 3*sqrt(2) / (PQ - PR)

t1 = check_term(1)  # should be 3/8
t2 = check_term(2)  # should be 3/15 = 1/5
assert simplify(t1 - Rational(3,8)) == 0
assert simplify(t2 - Rational(1,5)) == 0

if simplify(total - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('Got:', total)
