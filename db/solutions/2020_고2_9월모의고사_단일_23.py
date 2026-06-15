import sympy as sp
# x,7,y,13 등차. x+2y?
CANDIDATE = 24
x, y, d = sp.symbols('x y d')
sol = sp.solve([sp.Eq(7-x, d), sp.Eq(y-7, d), sp.Eq(13-y, d)], [x, y, d])
print('VERIFY_PASS' if sol[x]+2*sol[y] == CANDIDATE else 'VERIFY_FAIL')
