import sympy as sp
x = sp.Symbol('x')
P = x**2 - x - 2
R = 10*x + 11
Q1 = 2*x**3 + 3*x**2 + x + 1
Q2 = 3*x**3 + 8*x**2 + 3*x
Q3 = 5*x**3 + 12*x**2 + 3*x - 1
q1, rem1 = sp.div(Q1, P)
q2, rem2 = sp.div(Q2, P)
q3, rem3 = sp.div(Q3, P)
if sp.simplify(rem1 - R) == 0 and sp.simplify(rem2 - 2*R) == 0 and sp.simplify(rem3 - 3*R) == 0:
    result = P.subs(x, 3)
    if result == 4:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')