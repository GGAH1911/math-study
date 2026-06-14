from sympy import symbols, diff, simplify
x = symbols('x')
f = x**3 - 3*x - 1
g = x**4/2 - x**2
f_prime = diff(f, x)
g_prime = diff(g, x)
print('f(2)=', f.subs(x, 2))
print('g(2)=', g.subs(x, 2))
print('product=', f.subs(x,2) * g.subs(x,2))
print('g(0)=', g.subs(x,0))
print('g_prime(0)=', g_prime.subs(x,0))
g_double_prime = diff(g_prime, x)
print('g''(0)=', g_double_prime.subs(x,0))
print('g_prime(-x)+g_prime(x)=', simplify(g_prime.subs(x,-x) + g_prime.subs(x,x)))
if f.subs(x,2)*g.subs(x,2) == 4 and g.subs(x,0)==0 and g_double_prime.subs(x,0)<0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')