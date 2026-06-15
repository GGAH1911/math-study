from sympy import symbols, simplify, Rational, nsimplify
import sympy as sp

result = sp.Rational(1, 2) * 8**(sp.Rational(2, 3))
result_simplified = simplify(result)
print(result_simplified)

if result_simplified == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')