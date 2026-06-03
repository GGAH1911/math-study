from sympy import *
x = symbols('x', real=True)
f = 2*sin(pi*x/4)
# Points
A = Matrix([1, sqrt(2)])
B = Matrix([3, sqrt(2)])
C = Matrix([-3, -sqrt(2)])
# Verify C is on f(x)
assert simplify(f.subs(x, -3) - C[1]) == 0, 'C not on f(x)'
# Verify C is on line OB
slope = sqrt(2)/3
assert simplify(slope*(-3) - C[1]) == 0, 'C not on line OB'
# Vectors from A
AB = B - A
AC = C - A
# 2D cross product magnitude
cross = Abs(AB[0]*AC[1] - AB[1]*AC[0])
AB_mag = sqrt(AB.dot(AB))
AC_mag = sqrt(AC.dot(AC))
sin_theta = simplify(cross / (AB_mag * AC_mag))
expected = sqrt(3)/3
if simplify(sin_theta - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {sin_theta}, expected {expected}')
