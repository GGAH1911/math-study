from sympy import sqrt, simplify, Rational
from fractions import Fraction

CANDIDATE = 150

# Hyperbola parameters: a=3, c²=45 → b²=36
a = 3
c_squared = 45
b_squared = 36
c = sqrt(45)  # = 3√5

# Foci
F = (c, 0)  # (3√5, 0)
F_prime = (-c, 0)  # (-3√5, 0)

# Point coordinates (from verified solution)
P_x = 9*sqrt(5)/5
P_y = 12*sqrt(5)/5

Q_x = -7*sqrt(5)/5
Q_y = 4*sqrt(5)/5

R_x = 27*sqrt(5)/20
R_y = 3*sqrt(5)/10

# Verification 1: All points on hyperbola x²/9 - y²/36 = 1
def check_hyperbola(x, y):
    result = simplify(x**2/9 - y**2/36)
    return result

P_hyp = check_hyperbola(P_x, P_y)
Q_hyp = check_hyperbola(Q_x, Q_y)
R_hyp = check_hyperbola(R_x, R_y)

assert P_hyp == 1, f"P on hyperbola: {P_hyp} != 1"
assert Q_hyp == 1, f"Q on hyperbola: {Q_hyp} != 1"
assert R_hyp == 1, f"R on hyperbola: {R_hyp} != 1"

# Verification 2: P on circle x²+y²=c²=45
P_circle = simplify(P_x**2 + P_y**2)
assert P_circle == 45, f"P on circle: {P_circle} != 45"

# Verification 3: Q is 1:2 internal division of F'P
# Distance F'Q and QP
F_prime_Q_x = Q_x - F_prime[0]  # = Q_x + 3√5
F_prime_Q_y = Q_y - F_prime[1]
dist_F_prime_Q_sq = simplify(F_prime_Q_x**2 + F_prime_Q_y**2)

QP_x = P_x - Q_x
QP_y = P_y - Q_y
dist_QP_sq = simplify(QP_x**2 + QP_y**2)

dist_F_prime_Q = sqrt(dist_F_prime_Q_sq)
dist_QP = sqrt(dist_QP_sq)
ratio_FQ_QP = simplify(dist_F_prime_Q / dist_QP)
assert ratio_FQ_QP == Rational(1, 2), f"F'Q:QP = {ratio_FQ_QP} != 1:2"

# Verification 4: R on line FQ
# Parametric line: (x,y) = F + t(Q-F)
# Solve for parameter t from R
Q_minus_F_x = simplify(Q_x - c)
Q_minus_F_y = simplify(Q_y - 0)
t_from_x = simplify((R_x - c) / Q_minus_F_x)
y_check = simplify(0 + t_from_x * Q_minus_F_y)
assert simplify(R_y - y_check) == 0, f"R not on line FQ: y={R_y} vs check={y_check}"

# Verification 5: Calculate triangle QF'R area using shoelace formula
# Area = (1/2)|x₁(y₂-y₃) + x₂(y₃-y₁) + x₃(y₁-y₂)|
# Vertices: Q=(Q_x,Q_y), F'=(-c,0), R=(R_x,R_y)

term1 = Q_x * (0 - R_y)
term2 = (-c) * (R_y - Q_y)
term3 = R_x * (Q_y - 0)

area_2 = simplify(term1 + term2 + term3)
area = abs(simplify(area_2)) / 2

# Verification 6: Calculate 20S
S = area
result = 20 * S
result_simplified = simplify(result)

if result_simplified == CANDIDATE:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: Got {result_simplified}, expected {CANDIDATE}")