from fractions import Fraction
import sympy as sp

# 5^(3/2) / 5^(1/2) = 5^1 = 5 검증
result = sp.Pow(5, sp.Rational(3,2)) / sp.Pow(5, sp.Rational(1,2))
simplified = sp.simplify(result)

if simplified == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')