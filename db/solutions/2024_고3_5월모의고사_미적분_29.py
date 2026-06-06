CANDIDATE = 40

import sympy as sp
from sympy import sqrt, Rational, simplify

# Problem setup: Segment AB has length 3
# A = (0,0), C = (1,0) [divides AB at 1/3], D = (2,0) [divides AB at 2/3], B = (3,0)
# Circle ω: diameter BC, center D = (2,0), radius = 1

A = (0, 0)
C = (1, 0)
D = (2, 0)
B = (3, 0)

# Verify circle properties
BC_midpoint = ((B[0] + C[0])/2, 0)
assert BC_midpoint == (2, 0), "Circle center must be D"

BC_length = 3 - 1
radius = BC_length / 2
assert radius == 1, "Circle radius must be 1"

# Critical value: cos(θ₀) = 7/8 (from verified solution)
cos_theta_0 = Rational(7, 8)
sin_theta_0 = sqrt(1 - cos_theta_0**2)  # sqrt(15)/8

# Point P on circle at angle θ₀ from A
# Ray from A: (t cos θ, t sin θ) intersects circle (x-2)² + y² = 1
# Equation: t² - 4t cos θ + 3 = 0
# Solutions: t = 2cos θ ± sqrt(4cos² θ - 3)

discriminant_sqrt = sqrt(4*cos_theta_0**2 - 3)  # = 1/4
t_P = 2*cos_theta_0 + discriminant_sqrt  # = 2 (using positive root)

# P coordinates
P_x = t_P * cos_theta_0
P_y = t_P * sin_theta_0

# Verify P is on circle
P_on_circle = (P_x - 2)**2 + P_y**2 - 1
assert simplify(P_on_circle) == 0, "P must be on circle"

# Point Q: D is circle center, so line PD intersects circle at P and Q
# Q is reflection of P through center: Q = 2D - P
Q_x = 4 - P_x
Q_y = -P_y

# Verify Q is on circle
Q_on_circle = (Q_x - 2)**2 + Q_y**2 - 1
assert simplify(Q_on_circle) == 0, "Q must be on circle"

# Function f(θ) = |AQ|
f_squared = Q_x**2 + Q_y**2
f_squared = simplify(f_squared)
f_theta_0 = sqrt(f_squared)

# Compute derivative using implicit formula:
# f²(θ) = 13 - 8cos²θ - 4cosθ√(4cos²θ - 3)
# (f²)' = 16sinθcosθ + 4sinθ(8cos²θ - 3)/√(4cos²θ - 3)

f_squared_prime = simplify(
    16*sin_theta_0*cos_theta_0 + 
    4*sin_theta_0*(8*cos_theta_0**2 - 3)/discriminant_sqrt
)

# f'(θ) = (f²)'(θ) / (2f(θ))
f_derivative = simplify(f_squared_prime / (2*f_theta_0))

# a = f'(θ₀)
a = f_derivative

# Compute a²
a_squared = simplify(a**2)

# Extract integer answer
answer = int(a_squared)

# Verify
if answer == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")