from sympy import Rational, integrate, exp, sqrt, pi, oo, symbols, nsimplify
import sympy as sp

mu, sigma = 180, 20
x = sp.symbols('x')
pdf = 1/(sigma*sp.sqrt(2*sp.pi)) * sp.exp(-(x-mu)**2/(2*sigma**2))
# exact probability via standard normal table values used in problem
# P(190<=X<=210) = P(0.5<=Z<=1.5)
from sympy import erf
# P(0<=Z<=z) = 0.5*erf(z/sqrt(2))
def Phi0(z):
    return sp.Rational(1,2)*sp.erf(sp.Rational(z*10,10)/sp.sqrt(2))
z1 = sp.Rational(5,10)
z2 = sp.Rational(15,10)
prob = (sp.Rational(1,2)*sp.erf(z2/sp.sqrt(2))) - (sp.Rational(1,2)*sp.erf(z1/sp.sqrt(2)))
val = float(prob)
# table-based expected answer
table_val = 0.4332 - 0.1915
if abs(val - table_val) < 0.001 and abs(table_val - 0.2417) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')