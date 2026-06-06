import sympy as sp
x = sp.Symbol('x')
f_prime = 6*x**2 - 2*x
f = sp.integrate(f_prime, x)
C = sp.Symbol('C')
f_with_C = f + C
C_value = sp.solve(f_with_C.subs(x, 1) - 3, C)[0]
f_final = f + C_value
result = f_final.subs(x, 2)
if result == 14:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')