import math

def A(x, a, b):
    return a*x**2 + (a+b)*x + (a+b+1)

def B(x, a, b):
    return (a+b)*x**2 + (a+b+1)*x + a

def is_left_halfline(a, b, p, tol=1e-9):
    inside = [p - d for d in [1e-3, 0.1, 1, 10, 200]]
    outside = [p, p + 1e-3, p + 0.1, p + 1, p + 10, p + 200]
    for x in inside:
        if not (A(x, a, b) < -tol and B(x, a, b) < -tol):
            return False
    for x in outside:
        if A(x, a, b) < -tol and B(x, a, b) < -tol:
            return False
    return True

# ㄱ: a=-1, b=1 -> p=-1
assert is_left_halfline(-1, 1, -1), 'GA failed'

# ㄴ: every valid (a,b)=(a,-a) with a in [-1,0) has b>0 and solution {x<p}
for a in [-1.0, -0.9, -0.75, -0.5, -0.25, -0.1, -0.01]:
    b = -a
    p = -1.0/math.sqrt(-a)
    if not is_left_halfline(a, b, p):
        print('VERIFY_FAIL'); raise SystemExit
    if not (b > 0):
        print('VERIFY_FAIL'); raise SystemExit

# ㄷ False: (a,b)=(-0.5,0.5) is valid, but a^3 = -0.125 > -1
a, b = -0.5, 0.5
p = -1.0/math.sqrt(-a)
assert is_left_halfline(a, b, p)
assert a**3 > -1  # ㄷ does not hold universally

# Cross-check: for a=-1 with b != 1, solution is NOT {x<p}
# b=0: x=1 satisfies both (A=-2,B=-2) but should not be in {x<p<0}; confirms not a left half-line
assert A(1, -1, 0) < 0 and B(1, -1, 0) < 0
# b=2: x=-1.2 is in solution but x=-0.5 is not, while x=2.5 also in solution -> bounded interval, not {x<p}
assert A(-1.2, -1, 2) < 0 and B(-1.2, -1, 2) < 0
assert not (A(-3, -1, 2) < 0 and B(-3, -1, 2) < 0)  # large negative not in soln -> not left half-line

print('VERIFY_PASS')
