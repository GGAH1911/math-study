import numpy as np

# Given
A = np.array([2, 6])
B = np.array([6, 2])
C = np.array([4, 4])
D = np.array([8, 6])

Q = np.array([5, 9])
R = np.array([4, 1])

# Verify Q satisfies condition (가): on line x+y=14
assert abs(Q[0] + Q[1] - 14) < 1e-9, 'Q not on line'

# Verify Q satisfies condition (나): -4 <= x-y <= 4
assert -4 <= Q[0] - Q[1] <= 4, 'Q fails condition (나)'

# Verify R satisfies condition (가): on circle (x-4)^2+(y-4)^2=9
assert abs((R[0]-4)**2 + (R[1]-4)**2 - 9) < 1e-9, 'R not on circle'

# Verify R satisfies condition (나): -4 <= x-y <= 4
assert -4 <= R[0] - R[1] <= 4, 'R fails condition (나)'

# Verify Q achieves max y on S (compare with all candidate points)
# Max y on line segment: y at (5,9) and on arc: y at (4,7)
assert Q[1] >= 7, 'Q should have higher y than arc top (4,7)'

# Verify R achieves min y on S (compare with segment min y=5 and arc min y=1)
assert R[1] <= 5, 'R should have lower y than segment bottom (9,5)'

# Compute dot product
dot = int(Q[0]) * int(R[0]) + int(Q[1]) * int(R[1])
assert dot == 29, f'Expected 29, got {dot}'

print('VERIFY_PASS')
