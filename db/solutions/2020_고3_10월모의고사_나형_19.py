from sympy import sqrt, simplify

r = (6 - sqrt(6)) / 5

A = (0, r)
B = (-r*sqrt(3)/2, -r/2)
C = (r*sqrt(3)/2, -r/2)

cos_alpha = sqrt(3)*(3 + 2*sqrt(6))/18
sin_alpha = (2*sqrt(6) - 1)/6

D = (r*cos_alpha, r*sin_alpha)

def dist(p1, p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

AB = dist(A, B)
BD = dist(B, D)

BC_vec = (C[0]-B[0], C[1]-B[1])
BD_vec = (D[0]-B[0], D[1]-B[1])

cross = BC_vec[0]*BD_vec[1] - BC_vec[1]*BD_vec[0]
BC_mag = dist((0,0), BC_vec)
BD_mag = dist((0,0), BD_vec)

sin_angle = simplify(cross/(BC_mag*BD_mag))

if (simplify(sin_alpha**2 + cos_alpha**2 - 1) == 0 and
    simplify(BD - sqrt(2)) == 0 and
    simplify(sin_angle - sqrt(3)/3) == 0):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')