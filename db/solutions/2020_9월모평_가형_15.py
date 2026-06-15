import math

# Solution: a = 2*ln(2), b = 2
a = 2 * math.log(2)
b = 2

# Points
A = (a, math.exp(a))
B = (b, -math.log(b))

# Verify condition (나): OA · OB = 0
dot_product = A[0]*B[0] + A[1]*B[1]
print(f'OA · OB = {dot_product}')
assert math.isclose(dot_product, 0), f'Condition (나) failed: {dot_product}'

# Verify condition (가): |OA| = 2|OB|
OA = math.sqrt(A[0]**2 + A[1]**2)
OB = math.sqrt(B[0]**2 + B[1]**2)
print(f'|OA| = {OA}, 2|OB| = {2*OB}')
assert math.isclose(OA, 2*OB), f'Condition (가) failed'

# Calculate slope
slope = A[1] / A[0]
expected_slope = 2 / math.log(2)
print(f'Slope = {slope}')
print(f'2/ln(2) = {expected_slope}')
assert math.isclose(slope, expected_slope), f'Slope mismatch'

print('VERIFY_PASS')