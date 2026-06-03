import sympy as sp
x = sp.symbols('x', real=True)
a, b = 2, -1
f1 = a*x**2 + b*x + 1
f2 = -3*b*x - 1
# continuity at x=1
cont = sp.simplify(f1.subs(x,1) - f2.subs(x,1))
# differentiability at x=1
d1 = sp.diff(f1, x).subs(x,1)
d2 = sp.diff(f2, x).subs(x,1)
diff_eq = sp.simplify(d1 - d2)
ans = a + b
if cont == 0 and diff_eq == 0 and ans == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
