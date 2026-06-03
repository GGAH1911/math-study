from sympy import symbols, Rational, diff, simplify, solve, exp, Eq
t = symbols('t', real=True)
x = 2*exp(t) - 3*exp(-t)
y = 2*exp(t) + 6*exp(-t)
dydx = simplify(diff(y, t) / diff(x, t))
# Candidate answer
k_ans = 7
m_ans = Rational(2, 11)
total_ans = Rational(79, 11)
# Find all real t solving 2e^t + 6e^{-t} = k
u = symbols('u', positive=True)
roots_u = solve(2*u + 6/u - k_ans, u)
# Compute dy/dx at each root (substitute e^t = u)
vals = []
for ru in roots_u:
    val = simplify((2*ru**2 - 6)/(2*ru**2 + 3))
    vals.append(val)
vals_set = set(vals)
check1 = Rational(-1, 5) in vals_set
check2 = m_ans in vals_set
check3 = (k_ans + m_ans) == total_ans
if check1 and check2 and check3 and len(roots_u) == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
