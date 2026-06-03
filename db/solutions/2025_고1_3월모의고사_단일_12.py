import math
from math import sqrt

# Given values
AB = 13
BC = 11

# Calculate angle ABC from the constraint that triangle BCE has area 33
# Parallelogram area = 4 * (triangle BCE area) = 4 * 33 = 132
parallelogram_area = 132

# Parallelogram area = AB * BC * sin(angle_ABC)
sin_ABC = parallelogram_area / (AB * BC)
cos_ABC = sqrt(1 - sin_ABC**2)

# Verify sin(ABC) and cos(ABC)
assert abs(sin_ABC - 12/13) < 1e-9
assert abs(cos_ABC - 5/13) < 1e-9

# In parallelogram, AD = BC
AD = BC

# angle BAD = 180 - angle ABC
cos_BAD = -cos_ABC

# Using law of cosines in triangle ABD
BD_squared = AB**2 + AD**2 - 2*AB*AD*cos_BAD
BD = sqrt(BD_squared)

# Verify the answer
assert abs(BD - 20) < 1e-9
print('VERIFY_PASS')