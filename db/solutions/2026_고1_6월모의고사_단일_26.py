import sympy as sp

# 주어진 조건
a, b = 5, 6

# 이차방정식 x^2 + (a+1)x + b = 0의 근
x = sp.Symbol('x')
quadratic = x**2 + (a+1)*x + b
roots = sp.solve(quadratic, x)
alpha, beta = roots[0], roots[1]

# 조건 검증: α² + β² = 24
sum_of_squares = alpha**2 + beta**2
sum_of_squares_val = sp.simplify(sum_of_squares)

# 다항식 인수분해 검증
poly = x**3 + (a+2)*x**2 + (a**2 - 3*a + 2)*x + b
factored = (x + 1) * (x**2 + (a+1)*x + b)
expanded = sp.expand(factored)

if poly == expanded and sum_of_squares_val == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')