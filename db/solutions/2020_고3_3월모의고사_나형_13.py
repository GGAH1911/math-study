from sympy import symbols, expand, simplify
x, a = symbols('x a', real=True)
f = (x - a)**2
f_prime = 2*(x - a)
g = f - 3*f_prime
g_shifted = g.subs(x, -x)
eq = simplify(g - g_shifted)
a_val = -3
f_val = (x - a_val)**2
g_val = f_val - 3*2*(x - a_val)
g_val_simplified = simplify(expand(g_val))
print('g(x) =', g_val_simplified)
print('g(-x) =', simplify(expand(g_val_simplified.subs(x, -x))))
if g_val_simplified == simplify(expand(g_val_simplified.subs(x, -x))):
    result = f_val.subs(x, 0).subs(a, a_val)
    if result == 9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')