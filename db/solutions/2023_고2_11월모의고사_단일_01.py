from fractions import Fraction
import math

# 원래 식: 8^(-1/2) / sqrt(2)
original_result = (8**(-0.5)) / math.sqrt(2)
answer_value = Fraction(1, 4)

if abs(original_result - float(answer_value)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')