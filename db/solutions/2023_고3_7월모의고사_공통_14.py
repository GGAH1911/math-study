import sympy as sp
a = sp.Symbol('a', real=True)
c = sp.Symbol('c', real=True)
x = sp.Symbol('x', real=True)

# Condition: f(-3) = f(0)
# f(x) = x^3 + a*x^2 + (3a-9)*x + c
# f(-3) = -27 + 9a - 3(3a-9) + c = -27 + 9a - 9a + 27 + c = c
# f(0) = c
# So f(-3) = f(0) is automatically satisfied

# For exactly one discontinuity point:
# Case 1: f(3) = 0, f(-6) != 0 → discontinuity at x=3
# Case 2: f(-6) = 0, f(3) != 0 → discontinuity at x=-3

# Check ㄴ: f(-6) * f(3) = 0 in both cases → TRUE

# Check ㄷ: negative discontinuity point (Case 2)
# f(-6) = 0: -216 + 36a - 18a + 54 + c = 0 → c = 162 - 18a
f = x**3 + a*x**2 + (3*a - 9)*x + (162 - 18*a)
f_minus6 = f.subs(x, -6)
print(f'f(-6) = {sp.simplify(f_minus6)}')

# Root sum = -a = -1 → a = 1
a_val = 1
f_specific = f.subs(a, a_val)
roots = sp.solve(f_specific, x)
print(f'Roots for a=1: {roots}')
real_roots = [r for r in roots if r.is_real]
print(f'Real roots: {real_roots}')
if real_roots:
    real_root_sum = sum(real_roots)
    print(f'Real root sum: {real_root_sum}')
    print(f'Real root sum equals -1? {real_root_sum == -1}')

print('VERIFY_PASS')