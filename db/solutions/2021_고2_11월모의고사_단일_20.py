import numpy as np

def get_points(alpha, beta):
    A = np.array([alpha, 2**alpha])
    B = np.array([-alpha/2, 2**alpha])
    C = np.array([-beta, 2**(-beta)])
    D = np.array([beta/2, 2**(-beta)])
    return A, B, C, D

# ㄱ: a=b => AB=CD
alpha = 0.7; beta = alpha
A,B,C,D = get_points(alpha, beta)
assert abs(np.linalg.norm(A-B) - np.linalg.norm(C-D)) < 1e-9, 'ㄱ FAIL'

# ㄴ: 2m1 + m2 = 0 for various a,b
for al, be in [(0.5,0.8),(1.2,0.4),(2.0,3.0)]:
    A,B,C,D = get_points(al, be)
    m1 = (A[1]-C[1])/(A[0]-C[0])
    m2 = (B[1]-D[1])/(B[0]-D[0])
    assert abs(2*m1 + m2) < 1e-9, f'ㄴ FAIL al={al} be={be}'

# ㄷ: alpha=beta=0.5 satisfies AC⊥BD, slope(AD)=2√2, and ABCD is rhombus
alpha = 0.5; beta = 0.5
A,B,C,D = get_points(alpha, beta)
m1 = (A[1]-C[1])/(A[0]-C[0])
m2 = (B[1]-D[1])/(B[0]-D[0])
assert abs(m1*m2 + 1) < 1e-9, f'AC perp BD FAIL: m1*m2={m1*m2}'
slope_AD = (A[1]-D[1])/(A[0]-D[0])
assert abs(slope_AD - 2*np.sqrt(2)) < 1e-9, f'slope AD FAIL: {slope_AD}'
AB=np.linalg.norm(A-B); BC=np.linalg.norm(B-C)
CD=np.linalg.norm(C-D); DA=np.linalg.norm(D-A)
assert abs(AB-BC)<1e-9 and abs(BC-CD)<1e-9 and abs(CD-DA)<1e-9, f'Rhombus FAIL: {AB},{BC},{CD},{DA}'

print('VERIFY_PASS')