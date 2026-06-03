from sympy import symbols, Rational, solve
x, y = symbols('x y')
m = Rational(1-5, 1-(-2))  # slope = -4/3
# Line: y = m*x + b, use point (1,1)
b = 1 - m*1  # b = 1 - (-4/3) = 7/3
assert b == Rational(7, 3), f'y-intercept mismatch: {b}'
# Verify both points lie on the line
def f(xv): return m*xv + b
assert f(-2) == 5, f'Point (-2,5) check failed: f(-2)={f(-2)}'
assert f(1) == 1, f'Point (1,1) check failed: f(1)={f(1)}'
print('VERIFY_PASS')