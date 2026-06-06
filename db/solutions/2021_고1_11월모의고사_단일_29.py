import math
a = 16
h = 2 * math.sqrt(a)
B = (0, 0)
C = (a, 0)
A = ((a-4)/2, h)
D = ((a+4)/2, h)
AD = abs(D[0] - A[0])
assert AD == 4
BC = a
AB = math.sqrt(A[0]**2 + A[1]**2)
CD = math.sqrt((C[0] - D[0])**2 + (C[1] - D[1])**2)
assert abs(AB - CD) < 1e-10
center1 = ((B[0] + A[0])/2, (B[1] + A[1])/2)
r1 = AB / 2
center2 = ((C[0] + D[0])/2, (C[1] + D[1])/2)
dist = math.sqrt((center2[0] - center1[0])**2 + (center2[1] - center1[1])**2)
assert abs(dist - 2*r1) < 1e-10
S = (AD + BC) * h / 2
l = AD + BC + AB + CD
assert abs(S**2 + 8*l - 6720) < 1e-10
BD_squared = (D[0] - B[0])**2 + (D[1] - B[1])**2
assert abs(BD_squared - 164) < 1e-10
print('VERIFY_PASS')