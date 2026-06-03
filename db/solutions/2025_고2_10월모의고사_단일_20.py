import sympy as sp
from sympy import Rational, sqrt, simplify

# k^3 = -1/2 and a_1 = -2
k_cubed = Rational(-1, 2)
a1 = -2

# Verify k from the condition k = a_4 + a_5 - 1
k = k_cubed ** (sp.Rational(1, 3))
k = -sp.cbrt(sp.Rational(1, 2))

a2 = k * a1
a3 = k**2 * a1
a4 = k**3 * a1
a5 = k**4 * a1

# Check: k = a_4 + a_5 - 1
check1 = simplify(a4 + a5 - 1 - k)
if check1 == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')