from sympy import symbols, solve, Rational, Max, Min
x, a = symbols('x a', real=True)
f = -2*x**2 + 16*x - 7

def sum_max_min(a_val):
    a_val = Rational(a_val)
    # f on [0, a_val]: critical point x=4 if in range
    pts = [0, a_val]
    if 0 <= 4 <= a_val:
        pts.append(Rational(4))
    vals = [f.subs(x, p) for p in pts]
    return max(vals) + min(vals)

candidates = [1, 9]
ok = all(sum_max_min(c) == 0 for c in candidates)

# Also ensure no other positive a works by scanning analytically: solve in both regimes
sols_case1 = solve(-2*a**2 + 16*a - 14, a)  # case a<=4
sols_case2 = solve(-2*a**2 + 16*a + 18, a)  # case a>=8
valid = sorted({s for s in sols_case1 if 0 < s <= 4} | {s for s in sols_case2 if s >= 8})

total = sum(valid)
print('VERIFY_PASS' if ok and total == 10 and valid == [1, 9] else 'VERIFY_FAIL')
