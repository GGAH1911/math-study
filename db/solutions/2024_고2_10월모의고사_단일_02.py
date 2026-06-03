import sympy as sp
x = sp.Symbol('x')
# 조건: lim (f(x) - f(2)) / (x^2 - 4) = 3 as x -> 2
# 이는 f'(2) / 4 = 3 을 의미
# 따라서 f'(2) = 12

# 검증: f'(2) * (1/(x+2)) 의 극한
f_prime_2 = 12
expression = f_prime_2 / (x + 2)
limit_result = sp.limit(expression, x, 2)
if float(limit_result) == 3.0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')