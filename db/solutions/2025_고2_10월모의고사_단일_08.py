from sympy import log, sqrt, Rational
import math

# 원래 방정식: log_3(a) = 2*log_a(sqrt(3))
solutions = [3, Rational(1, 3)]

valid = True
for a_val in solutions:
    left = log(a_val, 3)
    right = 2 * log(sqrt(3), a_val)
    left_num = float(left)
    right_num = float(right)
    if abs(left_num - right_num) > 1e-10:
        valid = False
        break

total = sum(solutions)
if valid and total == Rational(10, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')