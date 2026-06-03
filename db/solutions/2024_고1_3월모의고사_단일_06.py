from sympy import symbols, expand
x, a, b = symbols('x a b')
polynomial = expand((x + a) * (x - 3))
print(f'전개 결과: {polynomial}')
a_val = -2
b_val = -5
result = expand((x + a_val) * (x - 3))
print(f'a=-2, b=-5일 때 전개: {result}')
if result == x**2 + b_val*x + 6:
    product = a_val * b_val
    print(f'ab = {product}')
    if product == 10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')