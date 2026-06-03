import sympy as sp
a, r = sp.symbols('a r', positive=True, real=True)
eq1 = sp.Eq(a**2 * r**2, 4)
eq2 = sp.Eq(a**2 * r**6, 64)
sol = sp.solve([eq1, eq2], [a, r])
print(f'Solution: {sol}')
for s in sol:
    a_val, r_val = s
    a6 = a_val * r_val**5
    print(f'a={a_val}, r={r_val}, a_6={a6}')
    if a6 == 32:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')