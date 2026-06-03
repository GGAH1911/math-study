from sympy import symbols, expand
x = symbols('x')
original = 2*x*(x+3) - (x**2 + 2*x - 1)
result = expand(original)
print(result)
coeff = result.as_coefficients_dict()[x]
print(f'x의 계수: {coeff}')
if coeff == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')