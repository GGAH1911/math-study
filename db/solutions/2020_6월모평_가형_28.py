CANDIDATE = 40  # 50*a, where a = lim_{theta->0+} (S1 - S2)/OH
import math

# ------------------------------------------------------------------
# 2020 6월모평 가형 28 (killer).
# AB = 2 is the diameter of a semicircle; O = midpoint of AB is the
# center (radius 1).  P is on arc AB with angle PAB = theta, so
# (since angle APB = 90) AP = 2 cos(theta).
# Q : intersection of the circle centered at A with radius AP and
#     segment AB  ->  Q = (AP, 0).
# R : point on arc PB with arc PR : arc RB = 3 : 7.
# T : intersection of segment OR with arc PQ (circle centered at A).
# H : foot of perpendicular from O to segment AP (= midpoint of AP).
# S1 : region bounded by PH, HO, OT and arc TP.
# S2 : region bounded by RT, QB and arcs TQ, BR.
# Goal:  a = lim_{theta->0+} (S1 - S2)/OH ,   answer = 50*a.
# We rebuild the whole construction from the geometry and take the
# limit by Richardson-style refinement; CANDIDATE must equal 50*a.
# ------------------------------------------------------------------

def green_straight(p1, p2):
    # (1/2)(x1*y2 - x2*y1): polygon-edge contribution to enclosed area
    return 0.5 * (p1[0] * p2[1] - p2[0] * p1[1])

def green_arc(center, r, a1, a2):
    # contribution of a circular arc (center C, radius r) from angle a1
    # to a2 to the enclosed area, via (1/2) integral (x dy - y dx)
    cx, cy = center
    I = (r * r * (a2 - a1)
         + cx * r * (math.sin(a2) - math.sin(a1))
         - cy * r * (math.cos(a2) - math.cos(a1)))
    return 0.5 * I

def angle_from(center, pt):
    return math.atan2(pt[1] - center[1], pt[0] - center[0])

def construct(theta):
    A = (0.0, 0.0)
    O = (1.0, 0.0)
    B = (2.0, 0.0)

    # P on circle (diameter AB), angle PAB = theta -> AP = 2 cos theta
    AP = 2.0 * math.cos(theta)
    P = (AP * math.cos(theta), AP * math.sin(theta))   # (2cos^2, 2cos sin)

    # Q on AB, circle centered at A radius AP
    Q = (AP, 0.0)

    # R on arc PB, arc PR : arc RB = 3:7.  Central angle of arc PB
    # (about O) is 2*theta (P sits at central angle 2theta, B at 0).
    # arc RB = (7/10)*(2theta) => R at central angle 7*theta/5.
    aR = 7.0 / 5.0 * theta
    R = (1.0 + math.cos(aR), math.sin(aR))

    # H: foot of perpendicular from O onto line AP (midpoint of AP here)
    d = (math.cos(theta), math.sin(theta))     # unit dir of AP
    tH = O[0] * d[0] + O[1] * d[1]
    H = (tH * d[0], tH * d[1])

    # T: intersection of segment OR with circle centered at A radius AP
    dx, dy = R[0] - O[0], R[1] - O[1]
    ox, oy = O[0] - A[0], O[1] - A[1]
    qa = dx * dx + dy * dy
    qb = 2.0 * (ox * dx + oy * dy)
    qc = ox * ox + oy * oy - AP * AP
    disc = qb * qb - 4.0 * qa * qc
    s = (-qb + math.sqrt(disc)) / (2.0 * qa)    # root inside segment (0<=s<=1)
    if not (-1e-9 <= s <= 1 + 1e-9):
        s = (-qb - math.sqrt(disc)) / (2.0 * qa)
    T = (O[0] + s * dx, O[1] + s * dy)

    rA = AP
    aP, aT, aQ = angle_from(A, P), angle_from(A, T), 0.0   # angles about A

    # S1 boundary: P -> H -> O -> T -> arc(T..P about A) -> P
    a1 = (green_straight(P, H) + green_straight(H, O) + green_straight(O, T)
          + green_arc(A, rA, aT, aP))
    S1 = abs(a1)

    # S2 boundary: R -> T (straight) -> arc(T..Q about A) -> Q -> B (straight)
    #              -> arc(B..R about O) -> R
    aB_O, aR_O = angle_from(O, B), angle_from(O, R)
    a2 = (green_straight(R, T) + green_arc(A, rA, aT, aQ)
          + green_straight(Q, B) + green_arc(O, 1.0, aB_O, aR_O))
    S2 = abs(a2)

    OH = math.sin(theta)
    return (S1 - S2) / OH

# Take the limit theta -> 0+ by sampling very small angles.
vals = [construct(t) for t in (1e-3, 1e-4, 1e-5, 1e-6)]
a_limit = vals[-1]               # converged value of a
answer = 50.0 * a_limit          # the quantity the problem asks for

# Sanity: the sequence must actually be converging (Cauchy), so this is
# a genuine limit and not a single fragile sample.
converging = all(abs(vals[i + 1] - vals[i]) < abs(vals[i] - vals[i - 1]) + 1e-9
                 for i in range(1, len(vals) - 1))

if converging and abs(answer - CANDIDATE) < 1e-3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL: 50a =', answer, 'candidate =', CANDIDATE)
