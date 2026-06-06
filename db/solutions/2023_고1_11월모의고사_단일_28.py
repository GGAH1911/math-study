import sympy as sp
from sympy import symbols, sqrt, expand, simplify

# Define variables
a, b, h = symbols('a b h', positive=True, real=True)

# Constraints
eq1 = a + b + h - 14
eq2 = a*b + a*h + b*h - 61

# Compute AC^2, CF^2, FA^2
AC_squared = a**2 + b**2
CF_squared = b**2 + h**2
FA_squared = a**2 + h**2

# Sum
total = AC_squared + CF_squared + FA_squared
total_simplified = expand(total)
print(f'AC^2 + CF^2 + FA^2 = {total_simplified}')

# Compute a^2 + b^2 + h^2 using the constraint
# (a+b+h)^2 = a^2 + b^2 + h^2 + 2(ab + ah + bh)
# 196 = a^2 + b^2 + h^2 + 2*61
# a^2 + b^2 + h^2 = 74

a_plus_b_plus_h_squared = 14**2
sum_products = 61 * 2
sum_squares = a_plus_b_plus_h_squared - sum_products
print(f'a^2 + b^2 + h^2 = {sum_squares}')

# The answer is 2 * (a^2 + b^2 + h^2)
answer = 2 * sum_squares
print(f'Answer: {answer}')

if answer == 148:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')