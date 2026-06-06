import numpy as np
from fractions import Fraction

a, b = Fraction(1, 2), Fraction(11, 10)

# Verify f(1/2) = alpha
f_half = (Fraction(1,4) - a + b**2)
alpha = b**2 - a**2
assert f_half == alpha, f'f(1/2)={f_half} != alpha={alpha}'

# Verify alpha + 24*beta = 30
beta = b**2
assert alpha + 24*beta == 30, f'alpha + 24*beta = {alpha + 24*beta}'

# Verify a < b
assert a < b, f'a={a} not < b={b}'

# Compute f(-2) and f(1)
f_neg2 = abs(-a*4 + b)
f_1 = 1 - 2*a + b**2
result = f_neg2 + f_1

# Check result is 211/100
assert result == Fraction(211, 100), f'f(-2)+f(1)={result}'

print('VERIFY_PASS')