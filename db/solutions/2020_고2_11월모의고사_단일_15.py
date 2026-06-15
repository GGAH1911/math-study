import sympy as sp
k = sp.symbols('k', positive=True, integer=True)
# a_n = (4 ** (1/(n+2))) ** (1/(n+1)) = 4 ** (1/((n+1)(n+2)))
total = sp.Integer(0)
for kk in range(1, 11):
    a_k = (sp.Integer(4) ** (sp.Rational(1, kk + 2))) ** (sp.Rational(1, kk + 1))
    term = sp.log(a_k, 2)
    total += sp.nsimplify(sp.simplify(term))
total = sp.simplify(total)
expected = sp.Rational(5, 6)
print('sum =', total)
if sp.simplify(total - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
