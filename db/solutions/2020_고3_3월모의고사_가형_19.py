from sympy import *

R = sqrt(10)
BC = 2*sqrt(5)

# sin(A) = BC/(2R) = 1/sqrt(2), acute => A = pi/4
A_val = pi/4
assert simplify(sin(A_val) - BC/(2*R)) == 0, 'sin A check failed'

# 3*sin(2C) = 4*sin(2B), B+C = 3*pi/4
# => tan(2B) = -3/4 with 2B in (pi/2, pi)
# => sin(2B) = 3/5, cos(2B) = -4/5
sin2B = Rational(3,5)
cos2B = Rational(-4,5)
assert sin2B**2 + cos2B**2 == 1

# cos(2B) = 1 - 2*sin^2(B) = -4/5 => sin^2(B) = 9/10
sinB = sqrt(Rational(9,10))
cosB = sqrt(Rational(1,10))
assert simplify(sinB**2 + cosB**2 - 1) == 0

# verify tan(2B) = -3/4
assert simplify(2*sinB*cosB/cos2B + Rational(3,4)) == 0, 'tan check'

# sin(C) = sin(A+B)
sinC = sin(A_val)*cosB + cos(A_val)*sinB
sinC = simplify(sinC)  # expect 2/sqrt(5)

# AB = 2R*sin(C)
AB = simplify(2*R*sinC)
print(f'AB = {AB}')

# verify all original conditions numerically
B_num = float(asin(sinB))
C_num = float(Rational(3,4)*pi) - B_num
A_num = float(A_val)
S1 = 5*float(sin(2*C_num))
S2 = 5*float(sin(2*B_num))
cond1 = abs(3*S1 - 4*S2) < 1e-8  # 3S1 = 4S2
cond2 = abs(2*float(R)*float(sin(A_num)) - float(BC)) < 1e-8  # BC = 2*sqrt(5)
cond3 = abs(float(AB) - 4*float(sqrt(2))) < 1e-8  # AB = 4*sqrt(2)
cond4 = 0 < B_num < float(pi/2) and 0 < C_num < float(pi/2)  # acute
print(f'3S1=4S2: {cond1}, BC=2√5: {cond2}, AB=4√2: {cond3}, acute: {cond4}')
if cond1 and cond2 and cond3 and cond4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
