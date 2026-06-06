import sympy as sp
x = sp.Symbol('x')
a_val = 3
b_val = 2

# 원래 문제 식
f = (x**2 + 4*x + a_val) / (x + 1)

# 극한값 검증
limit_result = sp.limit(f, x, -1)
print(f'극한값: {limit_result}')

# b값과 비교
if limit_result == b_val:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')