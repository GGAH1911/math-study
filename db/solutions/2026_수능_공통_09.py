import sympy as sp
x, a = sp.symbols('x a', real=True, positive=True)
f = x**3 + 3*a*x**2 - 9*a**2*x + 4
f_prime = sp.diff(f, x)
t = sp.symbols('t', real=True)
eq1 = f_prime.subs(x, t)
sol_t = sp.solve(eq1, t)
for t_val in sol_t:
    eq2 = f.subs(x, t_val) - 5
    sol_a = sp.solve(eq2, a)
    for a_val in sol_a:
        if a_val > 0:
            f_at_2 = f.subs([(x, 2), (a, a_val)])
            if f_at_2 == 14:
                print('VERIFY_PASS')
            else:
                print('VERIFY_FAIL')
            break