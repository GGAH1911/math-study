import sympy as sp
x = sp.Symbol('x')
f = x**3 - x**2 + 1
f_prime = sp.diff(f, x)
print('f(x) =', f)
print('f\'(x) =', f_prime)
print('Expected f\'(x) = 3x^2 - 2x:', f_prime == 3*x**2 - 2*x)
print('f(1) =', f.subs(x, 1), '(should be 1):', f.subs(x, 1) == 1)
f_2 = f.subs(x, 2)
print('f(2) =', f_2)
if f.subs(x, 1) == 1 and f_prime == 3*x**2 - 2*x and f_2 == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')