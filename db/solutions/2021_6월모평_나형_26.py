import sympy as sp
a = sp.Symbol('a')
f = a**3 - 3*a**2 + 5*a
avg_rate = f / a
f_prime_2 = 3*(2)**2 - 6*(2) + 5
eq = sp.Eq(avg_rate, f_prime_2)
sol = sp.solve(eq, a)
print('Solutions:', sol)
if 3 in sol:
    a_val = 3
    avg = (a_val**3 - 3*a_val**2 + 5*a_val) / a_val
    if abs(avg - f_prime_2) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')