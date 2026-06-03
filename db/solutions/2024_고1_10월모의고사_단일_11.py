from sympy import symbols, Rational, solve, Eq
a, b = symbols('a b', real=True)
Bx, By, Cx, Cy = symbols('Bx By Cx Cy', real=True)
Ax, Ay = 1, 2
# Midpoint AB = (6,7)
eq1 = Eq((Ax + Bx)/2, 6)
eq2 = Eq((Ay + By)/2, 7)
# Midpoint AC = (a,6)
eq3 = Eq((Ax + Cx)/2, a)
eq4 = Eq((Ay + Cy)/2, 6)
# Centroid = (5, b)
eq5 = Eq((Ax + Bx + Cx)/3, 5)
eq6 = Eq((Ay + By + Cy)/3, b)
sol = solve([eq1,eq2,eq3,eq4,eq5,eq6],[Bx,By,Cx,Cy,a,b],dict=True)[0]
val = sol[a] + sol[b]
print('VERIFY_PASS' if val == 10 else 'VERIFY_FAIL')
