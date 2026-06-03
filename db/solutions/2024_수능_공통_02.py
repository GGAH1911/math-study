import sympy as sp

x, h = sp.symbols('x h', real=True)
f = 2*x**3 - 5*x**2 + 3

# 미분의 정의를 이용한 극한 계산
f_2 = f.subs(x, 2)
f_2h = f.subs(x, 2 + h)
quotient = (f_2h - f_2) / h
limit_result = sp.limit(quotient, h, 0)

if limit_result == 4:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {limit_result}')