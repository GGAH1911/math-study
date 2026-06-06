from sympy import *
a = Rational(11, 4)
A = (-2, 4*a)
B = (2, 4*a)
C = (a-1, a*(a-1))
D = (a, a**2)
vertices = [A, C, D, B]
x_coords = [v[0] for v in vertices]
y_coords = [v[1] for v in vertices]
area = abs(sum(x_coords[i]*y_coords[(i+1)%4] - x_coords[(i+1)%4]*y_coords[i] for i in range(4))) / 2
M = area
result = 8 * M
if result == 121:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')