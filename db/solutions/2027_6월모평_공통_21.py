import sympy as sp

alpha = sp.Symbol('alpha')
f = lambda x: x**3 + 3*x**2 - 9*x + 9
f_prime = lambda x: 3*x**2 + 6*x - 9

answer = 11
result = f(2)

if result == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')