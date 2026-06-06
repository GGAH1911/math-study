from sympy import symbols, diff, simplify
x = symbols('x')
f = (x**2 - 2*x - 6) / (x - 1)
f_prime = diff(f, x)
result = f_prime.subs(x, 0)
if simplify(result - 8) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')