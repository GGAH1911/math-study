from sympy import symbols, expand

x = symbols('x')
a_value = 2

# 원래 식: (x^2 - 1/x) * (x + a/x^2)^4
# a = 2 대입
expr = (x**2 - 1/x) * (x + a_value/x**2)**4

# 전개
expanded = expand(expr)

# x^3의 계수 추출
coeff_x3 = expanded.coeff(x, 3)

# 검증: 계수가 7인가?
if coeff_x3 == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')