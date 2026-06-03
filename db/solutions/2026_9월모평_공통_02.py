import sympy as sp

# 원래 함수 정의
x, h = sp.symbols('x h')
f = x**2 - 4*x + 2

# f(4)와 f(4+h) 계산
f_at_4 = f.subs(x, 4)
f_at_4_plus_h = f.subs(x, 4 + h)

# 극한 계산: lim(h->0) [f(4+h) - f(4)] / h
difference_quotient = (f_at_4_plus_h - f_at_4) / h
limit_result = sp.limit(difference_quotient, h, 0)

print(f'f(4) = {f_at_4}')
print(f'f(4+h) = {f_at_4_plus_h}')
print(f'Difference quotient = {difference_quotient}')
print(f'Limit = {limit_result}')

if limit_result == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')