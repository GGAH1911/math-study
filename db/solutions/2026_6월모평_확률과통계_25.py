from sympy import symbols, expand, binomial

x = symbols('x')
polynomial = (2*x - 1)**5 * (x + 1)
expanded = expand(polynomial)

# x^3의 계수 추출
coeff_x3 = expanded.coeff(x, 3)
if coeff_x3 == 40:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')