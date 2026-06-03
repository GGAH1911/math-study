from sympy import *

# Given: sin(pi - theta) = 5/13 and cos(theta) < 0
# From sin(pi - theta) = sin(theta)
sin_theta = Rational(5, 13)

# Find cos(theta) from sin^2 + cos^2 = 1
cos_squared = 1 - sin_theta**2
cos_theta = -sqrt(cos_squared)  # negative due to cos(theta) < 0

print(f'sin(theta) = {sin_theta}')
print(f'cos(theta) = {cos_theta}')

# Calculate tan(theta)
tan_theta = sin_theta / cos_theta
print(f'tan(theta) = {tan_theta}')

# Verify the answer
if tan_theta == Rational(-5, 12):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')