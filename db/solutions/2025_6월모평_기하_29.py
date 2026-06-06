import numpy as np

a_sq = 5/4
c = 0.5
A = np.array([0, c + 1])
B = np.array([0, -c - 1])

# Q coordinates
y_Q = 22/3
x_Q_sq = (5/4) * (y_Q**2 - 1)
x_Q = np.sqrt(x_Q_sq)
Q = np.array([x_Q, y_Q])

# Verify hyperbola: y^2 - x^2/a^2 = 1
hyperbola_result = y_Q**2 - x_Q_sq / a_sq
assert abs(hyperbola_result - 1.0) < 1e-10, f'Hyperbola check failed: {hyperbola_result}'

# Verify AQ = 10
AQ = np.linalg.norm(Q - A)
assert abs(AQ - 10.0) < 1e-10, f'AQ check failed: {AQ}'

# Calculate perimeter
AB = np.linalg.norm(B - A)
BQ = np.linalg.norm(Q - B)
perimeter = AB + AQ + BQ

assert abs(perimeter - 25.0) < 1e-10, f'Perimeter check failed: {perimeter}'
print('VERIFY_PASS')