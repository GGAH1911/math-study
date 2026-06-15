import sympy as sp
# 등차 a1>0, a5=3a1, a1²+a3²=20. a5?
CANDIDATE = 6
a1, d = sp.symbols('a1 d', real=True)
sol = sp.solve([sp.Eq(a1+4*d, 3*a1), sp.Eq(a1**2+(a1+2*d)**2, 20)], [a1, d], dict=True)
s = [x for x in sol if x[a1] > 0][0]
print('VERIFY_PASS' if (a1+4*d).subs(s) == CANDIDATE else 'VERIFY_FAIL')
