import sympy as sp
b2 = 2 + 2*sp.sqrt(5)
c2 = 4 + b2
c = sp.sqrt(c2)
Px, Py = c, b2/2
PF = b2/2
QP_len = sp.Rational(5,3)*PF
Qx, Qy = c, Py + QP_len
Fpx, Fpy = -c, sp.Integer(0)
slope = (Qy - Fpy)/(Qx - Fpx)
Ry = slope*(0 - Fpx) + Fpy
QR = sp.sqrt((Qx)**2 + (Qy - Ry)**2)
diff = sp.simplify(QP_len - QR)
if diff == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: diff={diff}')