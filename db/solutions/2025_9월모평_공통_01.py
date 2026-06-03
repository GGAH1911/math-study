from fractions import Fraction

numerator = 32 ** Fraction(1, 4)
denominator = 4 ** Fraction(1, 8)
result = numerator / denominator

expected = 2

if result == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}, expected {expected}')