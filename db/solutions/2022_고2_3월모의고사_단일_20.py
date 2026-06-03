from sympy import *

x, y = symbols('x y')
m1 = Rational(-2, 1)
m2 = Rational(1, 2)
gak = bool(m1 * m2 == -1)

sol = solve([2*x + y + 2, x - 2*y - 4], [x, y])
A = (sol[x], sol[y])
B = (Rational(-1), S.Zero)
C = (Rational(4), S.Zero)

area_ABC = Abs(A[0]*(B[1]-C[1]) + B[0]*(C[1]-A[1]) + C[0]*(A[1]-B[1])) / 2

h, k = symbols('h k')
ds = lambda P, Q: (P[0]-Q[0])**2 + (P[1]-Q[1])**2
cc = solve([Eq(ds((h,k),A), ds((h,k),B)), Eq(ds((h,k),B), ds((h,k),C))], [h,k])
hc, kc = cc[h], cc[k]
r2 = ds((hc,kc), B)

py_val = Rational(6)
assert Rational(1,2)*(C[0]-B[0])*py_val == 3*area_ABC

Qy = py_val / 3
Qx = symbols('Qx')
Qx_sols = sorted(solve(Eq((Qx-hc)**2 + Qy**2, r2), Qx))

P_found = Q_found = None
for Qx_val in Qx_sols:
    px_val = 3*Qx_val - B[0] - C[0]
    if px_val > 0:
        P_found = (px_val, py_val)
        Q_found = (Qx_val, Qy)
        break

assert P_found is not None

centroid_ok = ((P_found[0]+B[0]+C[0])/3 == Q_found[0] and
               (P_found[1]+B[1]+C[1])/3 == Q_found[1])
circle_ok = ds(Q_found, (hc,kc)) == r2
area_ok = (Abs(P_found[0]*(B[1]-C[1])+B[0]*(C[1]-P_found[1])+C[0]*(P_found[1]-B[1]))/2
           == 3*area_ABC)
nae = bool(Q_found[1] == 2)
deut = bool(P_found[0]+P_found[1] == 10)

if gak and centroid_ok and circle_ok and area_ok and nae and not deut:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
