import sympy as sp

x, y = sp.symbols('x y', real=True)
# x=log2(a), y=log2(b)
# log_sqrt(a) b = 6  ->  (log2 b)/(log2 sqrt(a)) = y/(x/2) = 2y/x = 6
eq1 = sp.Eq(2*y, 6*x)
# log4 a + log2 b = 14 -> x/2 + y = 14
eq2 = sp.Eq(x/2 + y, 14)

sol = sp.solve([eq1, eq2], [x, y])
xval = sol[x]
yval = sol[y]

a = sp.Rational(2)**xval
b = sp.Rational(2)**yval

assert a > 1 and b > 1

lhs1 = sp.simplify(sp.log(b, sp.sqrt(a)))
assert sp.simplify(lhs1 - 6) == 0

lhs2 = sp.simplify(sp.log(a, 4) + sp.log(b, 2))
assert sp.simplify(lhs2 - 14) == 0

result = sp.simplify(sp.log(b/a, 2))

if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
