# (3x+1)^5 전개식에서 x^2 계수 a, x^3 계수 b → a+b?
import sympy as sp

x = sp.symbols('x')
poly = sp.Poly(sp.expand((3*x + 1)**5), x)
a = poly.coeff_monomial(x**2)
b = poly.coeff_monomial(x**3)
val = sp.Integer(a + b)
choices = {1: 315, 2: 330, 3: 345, 4: 360, 5: 375}
pick = [k for k, v in choices.items() if val == v]
print('VERIFY_PASS' if pick == [4] else 'VERIFY_FAIL')
