import numpy as np

a = 5
b = 1

# Test points in the supposed solution interval (1/5, 1)
test_inside = [0.3, 0.5, 0.7, 0.9]
# Test points outside the interval
test_outside_left = [0.1, 0.19, 0.0]
test_outside_right = [1.0, 1.5, 2.0]

def ineq1(x):
    return 4**x - 2**x - 2 < 0

def ineq2(x, a):
    import math
    if x <= 0:
        return False
    return math.log(x, a) + 1 > 0

# All inside points must satisfy BOTH inequalities
for x in test_inside:
    if not (ineq1(x) and ineq2(x, a)):
        print('VERIFY_FAIL'); exit()

# Boundary 1/5 should NOT satisfy (boundary excluded)
x_left = 1/5
if ineq2(x_left, a) and not ineq1(x_left):  # at boundary log_5(1/5)+1=0, not >0
    pass  # boundary not included, correct
if ineq2(x_left, a):  # log_5(1/5)+1 = -1+1 = 0, NOT >0, so False is correct
    print('VERIFY_FAIL'); exit()

# Boundary b=1 should NOT satisfy ineq1 (4^1-2^1-2=0, not <0)
if ineq1(b):
    print('VERIFY_FAIL'); exit()

# Points outside left boundary should fail ineq2
for x in test_outside_left:
    if x > 0 and ineq1(x) and ineq2(x, a):
        print('VERIFY_FAIL'); exit()

# Points outside right boundary should fail ineq1
for x in test_outside_right:
    if ineq1(x):
        print('VERIFY_FAIL'); exit()

print('VERIFY_PASS')
