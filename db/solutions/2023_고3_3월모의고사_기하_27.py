import sympy as sp

# Foci: F(0,4), F'(0,-4)
Fx, Fy = sp.Integer(0), sp.Integer(4)
Fpx, Fpy = sp.Integer(0), sp.Integer(-4)

# P = (6, 4)
Px, Py = sp.Integer(6), sp.Integer(4)

# Q = (-3*sqrt(11)/2, -7/2)
Qx = sp.Rational(-3,1)*sp.sqrt(11)/2
Qy = sp.Rational(-7,2)

PF       = sp.sqrt((Px-Fx)**2 + (Py-Fy)**2)
PF_prime = sp.sqrt((Px-Fpx)**2 + (Py-Fpy)**2)
QF       = sp.sqrt((Qx-Fx)**2 + (Qy-Fy)**2)
QF_prime = sp.sqrt((Qx-Fpx)**2 + (Qy-Fpy)**2)

P_hyp = Px**2/12 - Py**2/4   # should be -1
Q_hyp = Qx**2/12 - Qy**2/4   # should be -1

ok = (
    sp.simplify(P_hyp + 1) == 0 and
    sp.simplify(Q_hyp + 1) == 0 and
    sp.simplify(PF_prime - QF_prime - 5) == 0 and
    sp.simplify(PF - sp.Rational(2,3)*QF) == 0 and
    sp.simplify(PF + QF - 15) == 0
)
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')