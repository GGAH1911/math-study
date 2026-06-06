from sympy import symbols, expand
x = symbols('x')
a, b = 3, -1
lhs = x**2 + (a-1)*x - 1
rhs = x**2 + 2*x + b
diff = expand(lhs - rhs)
if diff == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')