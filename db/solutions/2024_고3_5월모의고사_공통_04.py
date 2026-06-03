from sympy import symbols, limit, diff, expand

h = symbols('h')

# 조건을 만족하는 함수의 예: f(x) = x^2 + x + 2
# f(1) = 1 + 1 + 2 = 4, f'(1) = 3
f_expr = (1 + 2*h)**2 + (1 + 2*h) + 2

# 극한 조건 검증
limit_expr = (f_expr - 4) / h
limit_val = limit(limit_expr, h, 0)

if limit_val == 6:
    # f(1) = 4 확인
    f_at_1 = 1**2 + 1 + 2
    # f'(1) = 3 확인
    f_prime_at_1 = 2*1 + 1
    
    answer = f_at_1 + f_prime_at_1
    if answer == 7:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')