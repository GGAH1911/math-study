from sympy import Rational, integrate, exp, sqrt, pi, oo, symbols, nsimplify
x = symbols('x')
mu = Rational(642,10)
sigma = Rational(4,10)
# normal pdf integrated from 65 to inf
pdf = 1/(sigma*sqrt(2*pi))*exp(-(x-mu)**2/(2*sigma**2))
prob = integrate(pdf, (x, 65, oo)).evalf()
# table-based value: 0.5 - P(0<=Z<=2.0)=0.5-0.4772
table_val = 0.5 - 0.4772
chosen = 0.0228
if abs(float(prob) - table_val) < 1e-3 and abs(table_val - chosen) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
