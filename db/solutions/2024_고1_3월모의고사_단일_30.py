from sympy import sqrt, simplify, symbols

# Points
A = (5, 10)
G = (13, 8)
F = (-3, 0)

# Vectors
GA = (A[0] - G[0], A[1] - G[1])
GF = (F[0] - G[0], F[1] - G[1])

# Magnitudes
mag_GA = (GA[0]**2 + GA[1]**2)**0.5
mag_GF = (GF[0]**2 + GF[1]**2)**0.5

# Cross product magnitude (2D)
cross_mag = abs(GA[0]*GF[1] - GA[1]*GF[0])

# sin(angle AGF)
sin_angle = cross_mag / (mag_GA * mag_GF)

# Expected value: 6/sqrt(85)
expected = 6 / sqrt(85)

# Verify
if abs(sin_angle - float(expected)) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')