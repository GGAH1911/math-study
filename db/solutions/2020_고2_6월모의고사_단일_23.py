import sympy as sp
# log2(x+5)=4. x?
CANDIDATE = 11
x = sp.symbols('x')
print('VERIFY_PASS' if sp.solve(sp.Eq(sp.log(x+5,2),4),x)[0]==CANDIDATE else 'VERIFY_FAIL')
