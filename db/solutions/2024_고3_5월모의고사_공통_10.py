from sympy import symbols, integrate, Rational

t = symbols('t', real=True)
v1 = 3*t**2 + 1
dist_P = integrate(v1, (t, 0, 2))  # 10

def dist_Q(mv):
    mv = Rational(mv)
    v2 = mv*t - 4
    if mv == 0:
        return integrate(4, (t, 0, 2))
    t0 = Rational(4) / mv
    if 0 < t0 < 2:
        return integrate(-v2, (t, 0, t0)) + integrate(v2, (t, t0, 2))
    # otherwise v2 has constant sign on [0,2]; v2(0)=-4<0 so |v2|=-v2 when t0>=2 or t0<=0
    return integrate(-v2, (t, 0, 2))

candidates = [-1, 8]
ok = all(dist_Q(mv) == dist_P for mv in candidates)

# Confirm no other real solutions exist by checking the two regime equations
from sympy import symbols as syms, solve, Eq
m = syms('m', real=True)
sol_neg = solve(Eq(8 - 2*m, 10), m)  # regime m<=2: only m=-1
sol_pos = solve(Eq(16/m + 2*m - 8, 10), m)  # regime m>2: m=1 or m=8, keep m>2
valid_neg = [s for s in sol_neg if s <= 2]
valid_pos = [s for s in sol_pos if s > 2]
all_m = sorted(valid_neg + valid_pos)

ok = ok and all_m == sorted(candidates) and sum(all_m) == 7
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
