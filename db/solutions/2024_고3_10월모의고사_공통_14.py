import sympy as sp
x = sp.Symbol('x')
f = x**4 - 2*x**3 + x**2 + 2*x + 1
f_prime = sp.diff(f, x)

# Case 1: t <= 1, f'(t) = 2
eq1 = sp.Eq(f_prime, 2)
sols_case1 = sp.solve(eq1, x)
sols_case1_filtered = [s for s in sols_case1 if s.is_real and s <= 1]

# Case 2: t > 1, f'(t-1) = 2
t = sp.Symbol('t')
f_prime_shifted = f_prime.subs(x, t-1)
eq2 = sp.Eq(f_prime_shifted, 2)
sols_case2 = sp.solve(eq2, t)
sols_case2_filtered = [s for s in sols_case2 if s.is_real and s > 1]

all_solutions = sorted(set(sols_case1_filtered + sols_case2_filtered))
total_sum = sum(all_solutions)

if abs(total_sum - 5) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')