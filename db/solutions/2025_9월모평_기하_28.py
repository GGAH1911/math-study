import sympy as sp

a = sp.Rational(10,1)*sp.sqrt(30)/3

# C1: x = 100/a  (from angle APO = pi/2)
x0 = sp.Rational(100,1) / a
# C2: y = 5*sqrt(2)  (from angle BQO = pi/2)
y0 = 5*sp.sqrt(2)

# z^2 for intersection points
z_sq = 100 - x0**2 - y0**2

N1 = (x0, y0, sp.sqrt(z_sq))
N2 = (x0, y0, -sp.sqrt(z_sq))

# Verify N1, N2 on sphere
assert sp.simplify(N1[0]**2 + N1[1]**2 + N1[2]**2 - 100) == 0, 'N1 not on sphere'
assert sp.simplify(N2[0]**2 + N2[1]**2 + N2[2]**2 - 100) == 0, 'N2 not on sphere'

# Verify angle APO = pi/2 at N1 (A=(a,0,0))
PA = (a - N1[0], -N1[1], -N1[2])
PO = (-N1[0], -N1[1], -N1[2])
dot_APO = PA[0]*PO[0] + PA[1]*PO[1] + PA[2]*PO[2]
assert sp.simplify(dot_APO) == 0, 'angle APO != pi/2'

# Verify angle BQO = pi/2 at N1 (B=(0,10*sqrt(2),0))
QB = (-N1[0], 10*sp.sqrt(2)-N1[1], -N1[2])
QO = (-N1[0], -N1[1], -N1[2])
dot_BQO = QB[0]*QO[0] + QB[1]*QO[1] + QB[2]*QO[2]
assert sp.simplify(dot_BQO) == 0, 'angle BQO != pi/2'

# Verify cos(angle N1 O N2) = 3/5
dot = N1[0]*N2[0] + N1[1]*N2[1] + N1[2]*N2[2]
cosval = sp.simplify(dot / 100)
if cosval == sp.Rational(3,5):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', cosval)
