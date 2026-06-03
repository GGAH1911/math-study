import sympy as sp
x = sp.Symbol('x')
f = 3*x**2 - 2*sp.sqrt(3)*x + 5
f_prime = sp.diff(f, x)
a = sp.solve(f_prime, x)[0]
m = f.subs(x, a)
result = m / a
result_simplified = sp.simplify(result)
if sp.simplify(result_simplified - 4*sp.sqrt(3)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')