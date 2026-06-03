from sympy import Rational, Abs, symbols, solve

a_val = 17

# Points
A = [a_val, -5, 2]
B = [2, 1, 1]

# P: internal division AB in ratio 2:1 (AP:PB = 2:1)
P = [(A[i] + 2*B[i]) / 3 for i in range(3)]

# Q: external division AB in ratio 2:1
Q = [(2*B[i] - A[i]) for i in range(3)]

# Midpoint M of PQ
M = [(P[i] + Q[i]) / 2 for i in range(3)]

# Distances to yz-plane (x=0) and zx-plane (y=0)
dist_yz = abs(M[0])  # distance to yz-plane
dist_zx = abs(M[1])  # distance to zx-plane

print(f'P = {P}')
print(f'Q = {Q}')
print(f'M = {M}')
print(f'dist to yz-plane = {dist_yz}')
print(f'dist to zx-plane = {dist_zx}')

if abs(dist_yz - dist_zx) < 1e-10 and a_val > 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
