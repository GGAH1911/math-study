import sympy as sp
x = sp.symbols('x')
# x<0 branch: a line that approaches the open circle at the origin (0,0)
left_line = sp.Rational(1,2)*x  # any line through origin; y-intercept (limit at 0-) is 0
# x>=1 branch: line through (1,-1) [filled dot] and (2,0): slope 1 -> f(x)=x-2
right_line = x - 2
lim_left = sp.limit(left_line, x, 0, '-')
lim_right = sp.limit(right_line, x, 1, '+')
result = sp.nsimplify(lim_left + lim_right)
CANDIDATE = sp.Integer(-1)
print('VERIFY_PASS' if sp.simplify(result - CANDIDATE) == 0 else 'VERIFY_FAIL')
