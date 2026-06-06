from sympy import symbols, diff
x = symbols('x')
f = x**3 + 7*x + 1
f_prime = diff(f, x)
result = f_prime.subs(x, 0)
if result == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')