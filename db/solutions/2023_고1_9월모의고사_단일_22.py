from sympy import symbols, expand
x = symbols('x')
f = x**3 - 3*x**2 + 3*x - 6
remainder = f.subs(x, 3)
print('VERIFY_PASS' if remainder == 3 else 'VERIFY_FAIL')