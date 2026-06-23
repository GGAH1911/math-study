import sympy as sp
x, a, c = sp.symbols('x a c', real=True)
f = x**3 + a*x**2 - 2 + c
f_prime = sp.diff(f, x)

# From integral equation at x=1: 0 = 1 + a - 2
a_val = sp.solve(1 + a - 2, a)[0]
print(f'a = {a_val}')

# f'(x) = 3x^2 + 2ax
f_prime_expr = f_prime.subs(a, a_val)
result = f_prime_expr.subs(x, a_val)
print(f'f\'({a_val}) = {result}')

if result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')