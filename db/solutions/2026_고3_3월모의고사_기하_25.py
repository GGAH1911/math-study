from sympy import *
import numpy as np

a = 2
A_sq = 5 * a**2
B_sq = a**2 + 1

A = sqrt(A_sq)
B = sqrt(B_sq)

asymptote_slope = B / A
expected_slope = Rational(1, 2)

assert simplify(asymptote_slope - expected_slope) == 0, f'Asymptote slope mismatch: {asymptote_slope} vs {expected_slope}'

major_axis_length = 2 * A
expected_answer = 4 * sqrt(5)

assert simplify(major_axis_length - expected_answer) == 0, f'Major axis length mismatch: {major_axis_length} vs {expected_answer}'

print('VERIFY_PASS')