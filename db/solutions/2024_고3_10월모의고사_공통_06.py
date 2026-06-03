import numpy as np
a, r = 3, 2
# Check a_3
assert a * r**2 == 12, 'a_3 condition failed'
# Calculate sums
S2 = a * (1 + r)
S4 = a * (1 + r + r**2 + r**3)
S6 = a * (1 + r + r**2 + r**3 + r**4 + r**5)
# Check main condition
assert 4 * (S4 - S2) == S6 - S4, 'Main condition failed'
# Calculate S3
S3 = a * (1 + r + r**2)
assert S3 == 21, 'S3 calculation failed'
print('VERIFY_PASS')