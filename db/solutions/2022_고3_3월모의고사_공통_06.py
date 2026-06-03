import sympy as sp

# 원래 함수 정의
x, a, h = sp.symbols('x a h')
f = 2*x**2 - 3*x + 5

# a = 2 확인
a_val = 2
avg_rate = (f.subs(x, a_val + 1) - f.subs(x, a_val)) / 1
assert abs(float(avg_rate) - 7) < 1e-9, f'Average rate should be 7, got {avg_rate}'

# 극한값 계산
limit_expr = (f.subs(x, a_val + 2*h) - f.subs(x, a_val)) / h
limit_val = sp.limit(limit_expr, h, 0)

if abs(limit_val - 10) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')