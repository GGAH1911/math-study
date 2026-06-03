import sympy as sp
x = sp.Symbol('x')
f = 2*x**3 - 3*x**2 + x

# Check conditions
print('f(0) =', f.subs(x, 0))
print('f(1) =', f.subs(x, 1))
f_prime = sp.diff(f, x)
print("f'(1) =", f_prime.subs(x, 1))

# Check limits
lim1 = sp.limit(f/x, x, 0)
lim2 = sp.limit(f/(x-1), x, 1)
print('lim f(x)/x as x->0:', lim1)
print('lim f(x)/(x-1) as x->1:', lim2)

# Answer
result = f.subs(x, 2)
print('f(2) =', result)

if lim1 == 1 and lim2 == 1 and f.subs(x, 0) == 0 and f.subs(x, 1) == 0 and f_prime.subs(x, 1) == 1 and result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')