from sympy import Rational, sqrt, solve, symbols, simplify, Abs
x = symbols('x', positive=True)
f = 2*sqrt(x)
g = Rational(1,4)*x**2
# A: nonzero intersection
sols = solve(f-g, x)
A_x = max([s for s in sols if s != 0])
A_y = f.subs(x, A_x)
assert simplify(A_y - g.subs(x, A_x)) == 0
# P divides OA in 1:3
Px = Rational(1,4)*A_x
Py = Rational(1,4)*A_y
# horizontal line y = Py meets f and g
Bx = solve(f - Py, x)[0]
Cx = solve(g - Py, x)[0]
By = Py; Cy = Py
# Area of triangle ABC
ax, ay = A_x, A_y
bx, by = Bx, By
cx, cy = Cx, Cy
area = Rational(1,2) * Abs((bx - ax)*(cy - ay) - (cx - ax)*(by - ay))
area = simplify(area)
expected = Rational(21, 8)
print('VERIFY_PASS' if area == expected else 'VERIFY_FAIL')
