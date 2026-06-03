from sympy import *

# Given
AB = Integer(2); BC = Integer(2); AD = Integer(3)
angle_BAD = pi/3

# Step 1: BD
BD_sq = AB**2 + AD**2 - 2*AB*AD*cos(angle_BAD)
assert simplify(BD_sq - 7) == 0

# Step 2: CD via cosine rule in triangle BCD (∠BCD = 2π/3)
angle_BCD = pi - angle_BAD
CD_sym = symbols('CD_sym', positive=True)
cd_eq = Eq(BD_sq, BC**2 + CD_sym**2 - 2*BC*CD_sym*cos(angle_BCD))
CD_val = [s for s in solve(cd_eq, CD_sym) if s > 0][0]
assert simplify(CD_val - 1) == 0, f'CD={CD_val}'
p = CD_val

# Step 3: ED via similarity (ratio 2:1)
# EB=2*ED, EC=2*ED-2, EA=ED+3=2*EC=4*ED-4 => ED=7/3
ED_sym = symbols('ED_sym', positive=True)
EC_expr = 2*ED_sym - 2
EA_expr = 2*EC_expr
ed_eq = Eq(EA_expr, ED_sym + AD)
ED_val = solve(ed_eq, ED_sym)[0]
assert simplify(ED_val - Rational(7,3)) == 0, f'ED={ED_val}'
q = ED_val

# Step 4: sinθ via sine rule in triangle ECD (∠ECD=π/3)
sin_theta = CD_val * sin(pi/3) / ED_val
sin_theta = simplify(sin_theta)
assert simplify(sin_theta - 3*sqrt(3)/14) == 0, f'sinθ={sin_theta}'

# Check sin²+cos²=1
cos_theta = sqrt(1 - sin_theta**2)
assert simplify(sin_theta**2 + cos_theta**2 - 1) == 0
r = sin_theta

# Step 5: (p+q)*r
result = simplify((p + q) * r)
expected = 5*sqrt(3)/7
if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}')