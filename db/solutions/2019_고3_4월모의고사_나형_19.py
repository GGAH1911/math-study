import sympy as sp

x = sp.symbols('x', real=True)
f = 1/(x+1) - 5
g = sp.sqrt(x+1)

# ㄱ: f(x) = -5 has no solution
solA = sp.solve(sp.Eq(f, -5), x)
A = (len(solA) == 0)

# ㄴ: integer y-coords on g over [0,8]
ys = set()
for y in range(0, 12):
    xv = y*y - 1  # solve sqrt(x+1)=y
    if 0 <= xv <= 8 and y >= 0:
        ys.add(y)
B = (len(ys) == 3)

# ㄷ: lattice points with integer x in [0,8], f(x) <= y <= g(x)
total = 0
for xi in range(0, 9):
    fv = sp.Rational(1, xi+1) - 5
    gv = sp.sqrt(sp.Integer(xi+1))
    lo = sp.ceiling(fv)
    hi = sp.floor(gv)
    total += int(hi - lo + 1)
C = (total == 61)

truth = (A, B, C)
mapping = {(True,False,False):1,(True,True,False):2,(True,False,True):3,(False,True,True):4,(True,True,True):5}
ans = mapping.get(truth, None)
print('A,B,C =', truth, '| total =', total, '| answer =', ans)
if ans == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
