from sympy import symbols, expand, Poly
x = symbols('x')
f = x**3 - 3*x**2 + 4*x - 3
P = -x**2 + 2*x - 2
Q = -x + 1
R = expand(P + Q**2)
lhs = expand(f)
rhs = expand(P*Q + R)
cond1 = expand(lhs - rhs) == 0
deg_R = Poly(R, x).degree() if R != 0 else -1
deg_P = Poly(P, x).degree()
deg_Q = Poly(Q, x).degree()
cond2 = deg_R < deg_P
cond3 = deg_R < deg_Q
cond4 = P.subs(x, 0) == -2
cond5 = Q.subs(x, 0) == 1
cond6 = f.subs(x, 2) == 1
if all([cond1, cond2, cond3, cond4, cond5, cond6]):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')