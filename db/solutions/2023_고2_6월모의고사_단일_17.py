import math

# Point P on y = sqrt(x), x > 0
a = 1/2
P = (a, math.sqrt(a))  # (0.5, sqrt(0.5))

# Distance OP
r = math.sqrt(P[0]**2 + P[1]**2)

# angle theta
theta = math.atan2(P[1], P[0])

# Check original condition: cos^2(theta) - 2*sin^2(theta) = -1
lhs = math.cos(theta)**2 - 2*math.sin(theta)**2
condition_ok = abs(lhs - (-1)) < 1e-9

# Check P on curve y = sqrt(x)
curve_ok = abs(P[1] - math.sqrt(P[0])) < 1e-9

# Expected answer: sqrt(3)/2
expected = math.sqrt(3)/2
answer_ok = abs(r - expected) < 1e-9

if condition_ok and curve_ok and answer_ok:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: lhs={lhs}, curve_check={curve_ok}, r={r}, expected={expected}')
