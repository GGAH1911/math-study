import math
from fractions import Fraction

# t = 5/3 (from PS = 2t = 10/3)
t = Fraction(5, 3)

# Compute p, q, r, s
p = 1 - t  # = -2/3
q = 1 - 1/t  # = 1 - 3/5 = 2/5
r = 1 + 1/t  # = 1 + 3/5 = 8/5
s = 1 + t  # = 1 + 5/3 = 8/3

print(f'p = {p}, q = {float(q):.4f}, r = {float(r):.4f}, s = {float(s):.4f}')

# Verify ordering p < q < r < s
assert p < Fraction(2, 5) < Fraction(8, 5) < s, 'Order check failed'

# Verify PS = 10/3
PS = float(s) - float(p)
assert abs(PS - 10/3) < 1e-10, f'PS check failed: {PS}'

# Compute QR
QR = Fraction(8, 5) - Fraction(2, 5)  # = 6/5
result = 30 * QR

print(f'QR = {QR}, 30 × QR = {result}')
assert result == 36, f'Result check failed: {result}'

print('VERIFY_PASS')