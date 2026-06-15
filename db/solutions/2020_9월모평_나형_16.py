from sympy import symbols, limit, oo, diff, solve, simplify

a = symbols('a', real=True)
x = symbols('x', real=True)

# f(x) = x^3 + a*x^2 + (2a-1)*x + a
f = x**3 + a*x**2 + (2*a-1)*x + a
f_prime = diff(f, x)

# Check first condition: lim_{x->inf} f(x)/x^3 = 1
lim1 = limit(f / x**3, x, oo)

# Check second condition: f(-1) = 0
f_at_minus1 = f.subs(x, -1)

# Check third condition: f'(-1) = 2
f_prime_at_minus1 = f_prime.subs(x, -1)

# Verify for a = 3
a_val = 3
f_func = x**3 + a_val*x**2 + (2*a_val-1)*x + a_val
f_at_1 = f_func.subs(x, 1)
f_at_2 = f_func.subs(x, 2)

print(f'lim x->inf f(x)/x^3 = {lim1} (should be 1)')
print(f'f(-1) = {f_at_minus1} (should be 0)')
print(f'f\'(-1) = {f_prime_at_minus1} (should be 2)')
print(f'For a=3: f(1) = {f_at_1} (should be <= 12)')
print(f'For a=3: f(2) = {f_at_2}')

if lim1 == 1 and f_at_1 <= 12 and f_at_2 == 33:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')