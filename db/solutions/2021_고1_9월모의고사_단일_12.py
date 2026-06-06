from sympy import *
alpha = 2 + 3*I
result = 1/alpha
result_simplified = simplify(result)
a = re(result_simplified)
b = im(result_simplified)
print(f'1/α = {result_simplified}')
print(f'a = {a}, b = {b}')
print(f'a+b = {a+b}')
if a + b == Rational(-1, 13):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')