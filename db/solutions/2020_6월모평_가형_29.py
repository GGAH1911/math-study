CANDIDATE = 24
# 2020 6월모평 가형 29 (평면벡터, 내적 영역 최적화)
#
# 곡선 C: y = sqrt(8 - x^2), 2 <= x <= 2*sqrt(2)  (원점 중심 반지름 2*sqrt(2) 원호)
#   -> P = 2*sqrt(2)*(cos t, sin t),  theta in [0, pi/4]
#      ( x = 2*sqrt(2) -> theta=0 ,  x = 2 -> cos = 1/sqrt(2) -> theta=pi/4 )
# OQ = 2, angle(POQ) = pi/4, Q는 직선 OP 아랫부분 -> Q는 각 (theta - pi/4), 크기 2
#   -> Q = 2*(cos(theta-pi/4), sin(theta-pi/4))
# X는 선분 OP 위 -> OX = s*OP,  s in [0,1]
# Y는 선분 OQ 위 -> OY = u*OQ,  u in [0,1]
# OZ = OP + OX + OY = (1+s)*OP + u*OQ
# R: 영역 D 중 y축과의 거리(|Zx|)가 최소인 점
# 구하는 값: OR.OZ 의 (max + min) = a + b*sqrt(2),  a+b = ?

import sympy as sp

th, s, u = sp.symbols('theta s u', real=True)
r = 2 * sp.sqrt(2)

P = sp.Matrix([r * sp.cos(th), r * sp.sin(th)])
Q = sp.Matrix([2 * sp.cos(th - sp.pi / 4), 2 * sp.sin(th - sp.pi / 4)])
Z = (1 + s) * P + u * Q  # OZ = OP + OX + OY

Zx = sp.expand_trig(Z[0])
Zy = sp.expand_trig(Z[1])

# --- R: minimize y축 거리 = |Zx| over s,u in [0,1], theta in [0,pi/4] ---
# Zx = (1+s)*2sqrt2*cos(theta) + u*2*cos(theta-pi/4).
# theta in [0,pi/4] -> cos(theta) >= 1/sqrt2 > 0 and cos(theta-pi/4) > 0,
# so every term of Zx is non-negative and Zx > 0. To minimize Zx take s=0, u=0,
# then Zx = 2sqrt2*cos(theta), minimal at theta = pi/4.
th_R = sp.pi / 4
R = sp.simplify(Z.subs({s: 0, u: 0, th: th_R}))
# Confirm this really is the argmin of |Zx| by checking the boundary candidates.
Zx_min_val = sp.nsimplify(Zx.subs({s: 0, u: 0, th: th_R}))
# sanity: Zx with s=0,u=0,theta=0 (larger) and any positive s,u only increase Zx
assert sp.simplify(Zx.subs({s: 0, u: 0, th: 0}) - Zx_min_val) > 0
assert sp.simplify(sp.diff(Zx, s).subs({th: th_R})) > 0  # increasing in s
assert sp.simplify(sp.diff(Zx, u).subs({th: th_R})) > 0  # increasing in u
# R must be (2,2)
assert R == sp.Matrix([2, 2]), R

# --- OR . OZ over the region ---
dot = sp.simplify(R.dot(Z))  # = 8*(1+s)*sin(theta+pi/4) + 4*sqrt2*u*sin(theta)
dds = sp.simplify(sp.diff(dot, s))  # 8*sin(theta+pi/4)
ddu = sp.simplify(sp.diff(dot, u))  # 4*sqrt2*sin(theta)

# For theta in [0,pi/4]: sin(theta+pi/4) > 0  => dot increasing in s (max s=1, min s=0)
#                        sin(theta) >= 0       => dot increasing in u (max u=1, min u=0)
assert sp.simplify(dds.subs(th, 0)) > 0 and sp.simplify(dds.subs(th, th_R)) > 0
assert sp.simplify(ddu.subs(th, 0)) >= 0 and sp.simplify(ddu.subs(th, th_R)) > 0

# MAX: s=1, u=1 ; then maximize f(theta) on [0,pi/4]
fmax = dot.subs({s: 1, u: 1})
# fmax = sqrt2*(12 sin th + 8 cos th); critical at atan(3/2) ~ 0.983 > pi/4,
# derivative > 0 on [0,pi/4] -> max at theta=pi/4
dfmax = sp.diff(fmax, th)
assert sp.simplify(dfmax.subs(th, 0)) > 0 and sp.simplify(dfmax.subs(th, th_R)) > 0
crit = sp.atan(sp.Rational(3, 2))
assert sp.N(crit) > sp.N(th_R)  # critical point outside interval
MAX = sp.nsimplify(sp.simplify(fmax.subs(th, th_R)))

# MIN: s=0, u=0 ; then minimize g(theta)=8 sin(theta+pi/4) on [0,pi/4]
# increasing in theta -> min at theta=0
fmin = dot.subs({s: 0, u: 0})
assert sp.simplify(sp.diff(fmin, th).subs(th, 0)) > 0  # increasing -> min at 0
MIN = sp.nsimplify(sp.simplify(fmin.subs(th, 0)))

total = sp.simplify(MAX + MIN)  # expect 20 + 4*sqrt2

# Extract a + b*sqrt(2) with a,b rational
poly = sp.Poly(sp.expand(total), sp.sqrt(2))
b = poly.coeff_monomial(sp.sqrt(2))
a = poly.coeff_monomial(1)
assert sp.simplify(total - (a + b * sp.sqrt(2))) == 0
answer = sp.nsimplify(a + b)

print("VERIFY_PASS" if sp.simplify(answer - CANDIDATE) == 0 else "VERIFY_FAIL")
