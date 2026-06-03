import sympy as sp

cos_theta = 2*sp.sqrt(78)/39
sin_theta = sp.sqrt(1 - cos_theta**2)

# Determine c, b^2 from problem geometry independent of answer
# Plane beta = xy-plane, AB on x-axis. Ellipse x^2/81 + y^2/b^2 = 1, foci (+-c,0)
# H = (H_x, H_y, 0); circle radius 4 tangent to AB => |H_y|=4, take H_y=4
# angle HFF' = pi/6 with sin = H_y/HF => HF = 8, cos => c - H_x = 4*sqrt(3)
# Q on line HF (param t with H at t=8) with HQ=4 and FQ>FH=8 => t_Q = 12
# Q = (c - 6*sqrt(3), 6). Focal sum FQ+F'Q = 2a = 18 => F'Q = 6
# F'Q^2 = (2c - 6*sqrt(3))^2 + 36 = 36 => c = 3*sqrt(3), b^2 = 81 - 27 = 54
c = 3*sp.sqrt(3)
b2 = sp.Integer(54)
H_x = c - 4*sp.sqrt(3)
H_y = sp.Integer(4)

# P on C1 has alpha-coords (u,v) with u^2+v^2=81
# 3D: P = (u, v*cos_theta, v*sin_theta). Foot of perp to beta: H = (u, v*cos_theta, 0)
# So u = H_x = -sqrt(3), v*cos_theta = H_y = 4 => v = 4/cos_theta
u = H_x
v = 4/cos_theta
residue_C1 = sp.simplify(u**2 + v**2 - 81)
if residue_C1 != 0:
    print('VERIFY_FAIL: P not on C1, residue =', residue_C1); raise SystemExit

# Build 3D points
P = sp.Matrix([u, v*cos_theta, v*sin_theta])
H = sp.Matrix([u, v*cos_theta, 0])
F = sp.Matrix([c, 0, 0]); Fp = sp.Matrix([-c, 0, 0])

# Verify HF = 8, HF' < HF, angle HFF' = pi/6
HF = sp.simplify(sp.sqrt((H-F).dot(H-F)))
HFp = sp.simplify(sp.sqrt((H-Fp).dot(H-Fp)))
if sp.simplify(HF - 8) != 0:
    print('VERIFY_FAIL: HF !=8, HF=', HF); raise SystemExit
if not (HFp < HF):
    print('VERIFY_FAIL: HF\' < HF fails:', HFp, HF); raise SystemExit

FH_v = H - F; FFp_v = Fp - F
cosA = sp.simplify(FH_v.dot(FFp_v)/(HF*sp.sqrt(FFp_v.dot(FFp_v))))
if sp.simplify(cosA - sp.sqrt(3)/2) != 0:
    print('VERIFY_FAIL: angle HFF\' != pi/6, cos=', cosA); raise SystemExit

# Verify Q on ellipse via original ellipse equation; Q closer to H; FQ > FH
t = sp.symbols('t', real=True)
udir = (H - F)/HF
pt = F + t*udir
ellipse = pt[0]**2/81 + pt[1]**2/b2 - 1
ts = sp.solve(sp.simplify(ellipse), t)
ts = [sp.nsimplify(sp.simplify(x)) for x in ts]
if len(ts) != 2:
    print('VERIFY_FAIL: ellipse intersections count =', ts); raise SystemExit
# Distances from H (param 8)
ds = [(sp.Abs(tv - 8), tv) for tv in ts]
ds.sort(key=lambda x: float(x[0]))
t_Q = ds[0][1]
Q = F + t_Q*udir
FQ = sp.Abs(t_Q); HQ = sp.Abs(t_Q - 8)
if not (FQ > HF):
    print('VERIFY_FAIL: FQ <= FH:', FQ, HF); raise SystemExit
if sp.simplify(HQ - 4) != 0:
    print('VERIFY_FAIL: HQ != 4:', HQ); raise SystemExit
# Circle radius 4 tangent to AB: dist from H to x-axis == 4
if sp.simplify(sp.Abs(H[1]) - 4) != 0:
    print('VERIFY_FAIL: H not at distance 4 from AB'); raise SystemExit
# Q indeed on ellipse (sanity)
if sp.simplify(Q[0]**2/81 + Q[1]**2/b2 - 1) != 0:
    print('VERIFY_FAIL: Q not on ellipse'); raise SystemExit
# P indeed on C1 in plane alpha: distance from origin in alpha = 9
alpha_dist2 = u**2 + v**2  # already checked
print('VERIFY_PASS')
