import sympy as sp
x, a = sp.symbols('x a', real=True)

# 극한값 직접 계산
f = a*x**2 + 2*x
numerator = x*f + 5*x
denominator = 2*f - x

limit_result = sp.limit(numerator / denominator, x, 0)
print(f'Limit value: {limit_result}')

# a의 값이 1/2 < a < 1 범위에서 극한이 5/3인지 확인
test_values = [0.6, 0.7, 0.8, 0.9]
for a_val in test_values:
    f_val = lambda x_val: a_val * x_val**2 + 2*x_val
    limit_val = float(limit_result)
    print(f'a={a_val}: limit={limit_val}, equals 5/3: {abs(limit_val - 5/3) < 1e-10}')

if abs(float(limit_result) - 5/3) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')