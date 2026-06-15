from sympy import symbols, expand, binomial

x = symbols('x')
expr = (2*x + 1/x**2)**4
expanded = expand(expr)

# 방법 1: 직접 전개
coeffs_dict = expanded.as_coefficients_dict()
coeff_x1 = coeffs_dict.get(x, 0)

# 방법 2: 이항정리로 검증
k = 1
coeff_binomial = binomial(4, k) * (2**(4-k))

if coeff_x1 == 32 and coeff_binomial == 32:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')