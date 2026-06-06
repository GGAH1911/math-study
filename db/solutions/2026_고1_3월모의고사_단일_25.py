from fractions import Fraction
import math

# 주어진 순환소수: 0.020202... = 2/99
p, q = 99, 2
assert math.gcd(p, q) == 1

# 검증: q/p가 0.020202...와 일치하는지
fraction_val = Fraction(q, p)
print(f'Fraction {q}/{p} = {float(fraction_val):.10f}')

# n = 30에서 조건 검증
n = 30
result = Fraction(6, p) * n + Fraction(q, 11)
print(f'(6/{p})*{n} + {q}/11 = {result}')

if result.denominator == 1 and result.numerator > 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')