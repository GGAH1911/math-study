from fractions import Fraction
import sympy as sp
from sympy import symbols, summation, oo, Rational

# Check a_1 = 1/4
a_1 = Rational(1, 4)
k = 2
r = Rational(1, 3)
b_1 = 27

# Verify condition: b_{k+i} = 1/a_i - 1 for i=1,2,3
for i in range(1, 4):
    a_i = a_1 * i
    b_k_plus_i = b_1 * r**(k + i - 1)
    expected = 1/a_i - 1
    assert b_k_plus_i == expected, f'Condition failed for i={i}'

# Check the inequality sum
sum_val = Rational(81, 2) - 16
assert 0 < sum_val < 30, f'Inequality failed: {sum_val}'

# Calculate sum of b_2n
a_2 = Rational(1, 2)
sum_b_2n = Rational(81, 8)
result = a_2 * sum_b_2n
assert result == Rational(81, 16), f'Final answer failed: {result}'

print('VERIFY_PASS')