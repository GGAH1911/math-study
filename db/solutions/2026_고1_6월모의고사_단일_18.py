import sympy as sp
t = sp.Symbol('t', positive=True)
sqrt3 = sp.sqrt(3)
H = (2/sqrt3 - t, sp.Integer(2))
J = (sp.Integer(2) + t - 2/sqrt3, sp.Integer(2))
I_ = (sp.Integer(0), sqrt3*t)
A = (sp.Integer(0), sp.Integer(2))
E = (sp.Integer(1), sqrt3*(t+1))
HJ = J[0] - H[0]
h_EHJ = E[1] - 2
area_EHJ = sp.Rational(1,2) * HJ * h_EHJ
AI = A[1] - I_[1]
h_AIH = H[0]
area_AIH = sp.Rational(1,2) * AI * h_AIH
S = sp.simplify(area_EHJ + area_AIH)
t_min = sp.solve(sp.diff(S, t), t)[0]
S_min = sp.simplify(S.subs(t, t_min))
answer = sqrt3/3
if sp.simplify(S_min - answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')