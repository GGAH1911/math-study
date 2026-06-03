from sympy import Rational, Abs

a = Rational(4, 5)

# Vertex A of f(x) = ax^2 - 4ax + 5a + 1  =>  a(x-2)^2 + (a+1)
A = (2, a + 1)

# Vertex B of g(x) = -x^2 - 2ax  =>  -(x+a)^2 + a^2
B = (-a, a**2)

# C = f(0) = 5a + 1  (y-intercept)
C = (0, 5*a + 1)

# O = origin
O = (0, 0)

def shoelace(pts):
    n = len(pts)
    total = 0
    for i in range(n):
        j = (i + 1) % n
        total += pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
    return Abs(total) / 2

area = shoelace([O, A, C, B])
if area == 7:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: area = {area}')
