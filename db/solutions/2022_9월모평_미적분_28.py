import math

A = (2.0, 0.0)
B = (0.0, -2.0)
AB = (B[0]-A[0], B[1]-A[1])
AB_norm = math.hypot(*AB)

def dot(u, v):
    return u[0]*v[0] + u[1]*v[1]

def sub(u, v):
    return (u[0]-v[0], u[1]-v[1])

def add(u, v):
    return (u[0]+v[0], u[1]+v[1])

def scale(s, u):
    return (s*u[0], s*u[1])

def norm(u):
    return math.hypot(*u)

def angle_PAB(alpha):
    # P on circle radius 2 at parameter alpha
    P = (2*math.cos(alpha), 2*math.sin(alpha))
    AP = sub(P, A)
    c = dot(AP, AB) / (norm(AP) * AB_norm)
    c = max(-1.0, min(1.0, c))
    return math.acos(c)

def find_P(theta_val):
    # bisection on alpha in [5pi/6, 7pi/6] (left half, ensures x<0)
    lo, hi = 5*math.pi/6, 7*math.pi/6
    # angle_PAB is decreasing on this interval (verified at endpoints: pi/3 -> pi/6)
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if angle_PAB(mid) > theta_val:
            lo = mid
        else:
            hi = mid
    alpha = 0.5*(lo+hi)
    P = (2*math.cos(alpha), 2*math.sin(alpha))
    # sanity: x_P < 0 and angle == theta_val
    assert P[0] < 0
    assert abs(angle_PAB(alpha) - theta_val) < 1e-8
    return P

def f(theta_val):
    P = find_P(theta_val)
    Q = (0.0, 2*math.cos(theta_val))
    BP = sub(P, B)
    BQ = sub(Q, B)
    t = dot(BQ, BP) / dot(BP, BP)
    R = add(B, scale(t, BP))
    return norm(sub(P, R))

def simpson(func, a, b, n=400):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = func(a) + func(b)
    for i in range(1, n):
        x = a + i*h
        s += 4*func(x) if i % 2 == 1 else 2*func(x)
    return s * h / 3

integral = simpson(f, math.pi/6, math.pi/3, n=400)
expected = (2*math.sqrt(3) - 3) / 2

if abs(integral - expected) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'computed={integral} expected={expected}')
    print('VERIFY_FAIL')
