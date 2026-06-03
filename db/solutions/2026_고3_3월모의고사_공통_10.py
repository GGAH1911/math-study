from sympy import *
k = Integer(2)
A = (k+1, Integer(0))
B = (k+4, Integer(2))
C = (Integer(0), Integer(2))
AB = sqrt((B[0]-A[0])**2 + (B[1]-A[1])**2)
AC = sqrt((C[0]-A[0])**2 + (C[1]-A[1])**2)
bx, by = B[0]-A[0], B[1]-A[1]
cx, cy = C[0]-A[0], C[1]-A[1]
area = Rational(1,2)*Abs(bx*cy - by*cx)
if AB == AC and area == 6 and k > 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')