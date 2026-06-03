import sympy as sp
x = sp.Symbol('x')
f = x**2 - 5*x + 4
f_at_6 = f.subs(x, 6)
print('f(6) =', f_at_6)
eq1 = f
roots1 = sp.solve(eq1, x)
product_roots = roots1[0] * roots1[1]
print('Product of roots of f(x)=0:', product_roots)
eq2 = f - (-x + 1)
roots2 = sp.solve(eq2, x)
diff_roots = abs(roots2[0] - roots2[1])
print('Difference of roots of f(x)=-x+1:', diff_roots)
if f_at_6 == 10 and product_roots == 4 and diff_roots == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')