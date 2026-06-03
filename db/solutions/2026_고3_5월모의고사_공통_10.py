import numpy as np

AB = 4
AC = 15
area = 24

# sin A from area
sinA = area / (0.5 * AB * AC)
assert abs(sinA - 4/5) < 1e-9, f'sinA wrong: {sinA}'

# A is acute => cosA > 0
cosA = np.sqrt(1 - sinA**2)
assert cosA > 0, 'A must be acute'

# BC via cosine rule
BC2 = AB**2 + AC**2 - 2*AB*AC*cosA
BC = np.sqrt(BC2)
assert abs(BC - 13) < 1e-9, f'BC wrong: {BC}'

# Circumradius via sine rule
R = BC / (2 * sinA)
assert abs(R - 65/8) < 1e-9, f'R wrong: {R}'

# Verify area with these values
computed_area = 0.5 * AB * AC * sinA
assert abs(computed_area - 24) < 1e-9, f'area wrong: {computed_area}'

print('VERIFY_PASS')
