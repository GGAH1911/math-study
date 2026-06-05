import math
A = (-1, 1, -2)
B = (2, 4, 1)
# Line AB: (x,y,z) = A + t(B-A)
# At xy-plane, z=0
# -2 + t(1-(-2)) = 0
# -2 + 3t = 0
t = 2/3
P = (A[0] + t*(B[0]-A[0]), A[1] + t*(B[1]-A[1]), A[2] + t*(B[2]-A[2]))
assert P[2] == 0, f'P z-coordinate should be 0, got {P[2]}'
AP_length = math.sqrt((P[0]-A[0])**2 + (P[1]-A[1])**2 + (P[2]-A[2])**2)
expected = 2*math.sqrt(3)
if abs(AP_length - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')