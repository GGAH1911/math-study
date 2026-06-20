from sympy import symbols, expand, binomial

x = symbols('x')

# 방법1: 전개식으로 계산
poly = expand((1 + 2*x)**4)
coeff_from_expand = poly.coeff(x, 2)

# 방법2: 이항정리로 계산
k = 2
n = 4
coeff_calculated = binomial(n, k) * (2**k)

# 검증
if coeff_from_expand == coeff_calculated == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')