import sympy as sp
import numpy as np

x, p, c = sp.symbols('x p c', real=True)

# f(x) = x^3/3 - x^2 + c with c = f(0)
f = x**3/3 - x**2 + c
f_prime = sp.diff(f, x)

# Verify f'(0) = f'(2) = 0
assert f_prime.subs(x, 0) == 0
assert f_prime.subs(x, 2) == 0

# Check 가: p=1, g'(1)=0
p_val = 1
g_prime_at_1 = f_prime.subs(x, 1 + p_val)
assert g_prime_at_1 == 0, f"가 실패: {g_prime_at_1}"

# Check 나: f'(p)=0 for p>0 -> p=2 unique
f_prime_p = f_prime.subs(x, p)
roots = sp.solve(f_prime_p, p)
positive_roots = [r for r in roots if r > 0]
assert len(positive_roots) == 1 and positive_roots[0] == 2, f"나 실패: {positive_roots}"

# Check 다: p>=2, integral >= 0
p_var = sp.Symbol('p', positive=True, real=True)
f_expr = x**3/3 - x**2
integral_1 = sp.integrate(f_expr, (x, -1, 0))
integral_2 = sp.integrate(f_expr.subs(x, x + p_var), (x, 0, 1)) - sp.integrate(f_expr.subs(x, p_var), (x, 0, 1))
total = integral_1 + integral_2
total_simplified = sp.simplify(total)

# For p=2: check >= 0
for p_test in [2, 3, 4]:
    val = float(total_simplified.subs(p_var, p_test))
    assert val >= -1e-10, f"다 실패 at p={p_test}: {val}"

print('VERIFY_PASS')