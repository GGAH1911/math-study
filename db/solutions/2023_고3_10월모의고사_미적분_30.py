import sympy as sp
x = sp.Symbol('x')
a, b = -1, 1
f = (x**2 + a*x + b) * sp.exp(-x)

# f(10)을 계산
f_10 = f.subs(x, 10)
print(f'f(10) = {f_10}')

# p 추출 (f(10) = p * e^(-10) 형태)
p = (100 + (-1)*10 + 1)
print(f'p = {p}')

# 검증: f(10) = p * e^(-10)인지 확인
verify = sp.simplify(f_10 - p * sp.exp(-10))
if verify == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')