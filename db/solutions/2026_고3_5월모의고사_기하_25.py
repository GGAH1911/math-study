import numpy as np

c = np.sqrt(3)
a = 3
b_sq = a**2 - c**2  # should be 6
b = np.sqrt(b_sq)

# Pick P in 1st quadrant, Q in 2nd quadrant on the ellipse
t_P = np.pi / 4
Px = a * np.cos(t_P)
Py = b * np.sin(t_P)

t_Q = 2 * np.pi / 3
Qx = a * np.cos(t_Q)
Qy = b * np.sin(t_Q)

F  = np.array([c, 0.0])
Fp = np.array([-c, 0.0])
P  = np.array([Px, Py])
Q  = np.array([Qx, Qy])

# Find intersection R of segment PF' and segment QF
# P + s*(Fp - P) = Q + t*(F - Q)
A_mat = np.column_stack([Fp - P, -(F - Q)])
b_vec = Q - P
params = np.linalg.solve(A_mat, b_vec)
s, t = params

R = P + s * (Fp - P)

PR  = np.linalg.norm(R - P)
RF  = np.linalg.norm(F - R)
PF  = np.linalg.norm(F - P)
QR  = np.linalg.norm(R - Q)
RFp = np.linalg.norm(Fp - R)
QFp = np.linalg.norm(Fp - Q)

perim_PRF  = PR + RF + PF
perim_QFpR = QR + RFp + QFp
total = perim_PRF + perim_QFpR

# Verify minor axis = 2*sqrt(6)
minor_axis = 2 * b
pass1 = abs(total - 12.0) < 1e-9
pass2 = abs(b_sq - 6.0) < 1e-12
pass3 = abs(minor_axis - 2*np.sqrt(6)) < 1e-12

if pass1 and pass2 and pass3:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: total={total}, b^2={b_sq}, 2b={minor_axis}')
