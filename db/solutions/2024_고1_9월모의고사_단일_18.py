from sympy import symbols, expand, simplify
x = symbols('x')
f = x**5 + 2*x**4 + x**3
result = f.subs(x, 1)
if result == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')