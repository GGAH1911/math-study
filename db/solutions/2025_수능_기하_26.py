import sympy as sp

x, y, t = sp.symbols('x y t', real=True)

count = 0
valid = []
for n in range(2, 100):
    # line x = 1/n
    xv = sp.Rational(1, n)
    # P on C1: x^2/2 + y^2 = 1, first quadrant
    yP_sq = 1 - xv**2/2
    if yP_sq <= 0:
        continue
    yP = sp.sqrt(yP_sq)
    # Q on C2: 2x^2 + y^2/2 = 1, first quadrant
    yQ_sq = 2*(1 - 2*xv**2)
    if yQ_sq <= 0:
        continue
    yQ = sp.sqrt(yQ_sq)
    # tangent to C1 at P: x*xP/2 + y*yP = 1; implicit diff to verify
    # using formula: x*x0/a^2 + y*y0/b^2 = 1
    # C1: a^2=2, b^2=1
    # x-intercept (y=0): x*xv/2 = 1 -> x = 2/xv = 2n
    alpha = 2/xv
    # C2: a^2=1/2, b^2=2
    # tangent: x*xv/(1/2) + y*yQ/2 = 1 -> 2*xv*x + y*yQ/2 = 1
    # x-intercept: 2*xv*x = 1 -> x = 1/(2*xv) = n/2
    beta = 1/(2*xv)
    diff = sp.simplify(alpha - beta)
    if 6 <= diff <= 15:
        count += 1
        valid.append(n)

# Cross-check tangent x-intercepts via implicit differentiation for one case
n_test = 5
xv = sp.Rational(1, n_test)
yP = sp.sqrt(1 - xv**2/2)
# C1: x^2/2 + y^2 = 1 => dy/dx = -x/(2y)
slope1 = -xv/(2*yP)
# tangent: y - yP = slope1*(x - xv); y=0 => x = xv - yP/slope1
alpha_check = sp.simplify(xv - yP/slope1)
assert sp.simplify(alpha_check - 2*n_test) == 0, f'alpha mismatch: {alpha_check}'

yQ = sp.sqrt(2*(1 - 2*xv**2))
# C2: 2x^2 + y^2/2 = 1 => 4x + y*y' = 0 => y' = -4x/y
slope2 = -4*xv/yQ
beta_check = sp.simplify(xv - yQ/slope2)
assert sp.simplify(beta_check - sp.Rational(n_test,2)) == 0, f'beta mismatch: {beta_check}'

if count == 7 and valid == [4,5,6,7,8,9,10]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', count, valid)
