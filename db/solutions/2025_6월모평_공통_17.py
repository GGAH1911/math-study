from sympy import symbols, diff, integrate
x = symbols('x')
f_prime = 6*x**2 + 2
f = integrate(f_prime, x) + 3
print(f'f(x) = {f}')
print(f'f\'(x) = {diff(f, x)}')
print(f'f(0) = {f.subs(x, 0)}')
result = f.subs(x, 2)
print(f'f(2) = {result}')
if diff(f, x) == f_prime and f.subs(x, 0) == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')