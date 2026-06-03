import sympy as sp

a = sp.log(3)
x = sp.symbols('x', real=True)

f_hi = (x - a - 2)**2 * sp.exp(x)        # x >= a
f_lo = sp.exp(2*a)*(x - a) + 4*sp.exp(a) # x < a

# continuity at a
assert sp.simplify(f_hi.subs(x, a) - f_lo.subs(x, a)) == 0

# critical structure
fp_hi = sp.diff(f_hi, x)
assert sp.simplify(fp_hi - (x-a-2)*(x-a)*sp.exp(x)) == 0

# local max f(a) = 4 e^a = 12
assert sp.simplify(f_hi.subs(x, a) - 12) == 0
# local min f(a+2) = 0
f_a2 = sp.simplify(f_hi.subs(x, a+2))
assert f_a2 == 0

# value at a+6
f_a6 = sp.simplify(f_hi.subs(x, a+6))   # 16 * e^(a+6) = 48 e^6
assert sp.simplify(f_a6 - 48*sp.exp(6)) == 0
assert sp.simplify(f_a6 - 12) > 0  # in increasing branch region

# g'(f(a+2)) = g'(0): smallest x with f(x)=0 is on linear branch (x = a - 4 e^{-a})
# inverse of linear branch: g(t) = a + (t - 4 e^a) e^{-2a}; g'(t) = e^{-2a}
gp_at_0 = sp.exp(-2*a)
assert sp.simplify(gp_at_0 - sp.Rational(1,9)) == 0

# verify a - 4 e^{-a} is indeed < a+2 (true) and gives f = 0
x0_lin = a - 4*sp.exp(-a)
assert sp.simplify(f_lo.subs(x, x0_lin)) == 0

# g'(f(a+6)): on increasing branch, g(f(a+6)) = a+6, g'(t) = 1/f'(a+6)
fp_a6 = sp.simplify(fp_hi.subs(x, a+6))   # 24 e^(a+6) = 72 e^6
assert sp.simplify(fp_a6 - 72*sp.exp(6)) == 0
gp_at_fa6 = 1/fp_a6

ratio = sp.simplify(gp_at_0 / gp_at_fa6)
target = 8*sp.exp(6)
if sp.simplify(ratio - target) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
