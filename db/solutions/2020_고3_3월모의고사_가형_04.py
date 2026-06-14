from sympy import symbols, diff, limit
x, h = symbols('x h')
f = x**3 - x**2
f_prime = diff(f, x)
result = f_prime.subs(x, 2)
print(f'f\'(2) = {result}')
if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')