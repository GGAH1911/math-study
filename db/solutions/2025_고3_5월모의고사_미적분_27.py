import sympy as sp

# Step 1: x=0에서 e^{2f(0)} - e^{f(0)} - 2 = 0
t = sp.Symbol('t', positive=True)
eq1 = t**2 - t - 2
roots = sp.solve(eq1, t)
assert 2 in roots
e_f0 = 2  # e^{f(0)}

# Step 2: 미분 후 x=0 대입: 2b*(e_f0)^2 - 2b*e_f0 - 6 = 0
b = sp.Symbol('b')
eq2 = 2*b*(e_f0**2) - 2*b*e_f0 - 6
# = 2b*4 - 2b*2 - 6 = 8b - 4b - 6 = 4b - 6
f_prime_0_sols = sp.solve(eq2, b)
assert len(f_prime_0_sols) == 1
f_prime_0 = f_prime_0_sols[0]  # 3/2

# Step 3: g'(f(0)) = 1/f'(0)
g_prime_f0 = sp.Rational(1, 1) / f_prime_0

# 검증: 원래 함수 f(x) = (3/2)x + ln2가 방정식을 만족하는지 확인
x = sp.Symbol('x')
f = sp.Rational(3, 2)*x + sp.ln(2)
lhs = sp.exp(2*f) - sp.exp(f.subs(x, 2*x)) - 2*sp.exp(3*x)
lhs_simplified = sp.simplify(lhs)

expected = sp.Rational(2, 3)
if lhs_simplified == 0 and sp.simplify(g_prime_f0 - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'lhs={lhs_simplified}, g_prime_f0={g_prime_f0}')
    print('VERIFY_FAIL')
