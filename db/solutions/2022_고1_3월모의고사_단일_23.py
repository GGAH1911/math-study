import sympy as sp
x = sp.Symbol('x')
a = 8
# 원래 다항식
poly = x**2 - 2*x - 80
# (x+a)로 나누어떨어지는지 확인
factored = sp.factor(poly)
print(f'인수분해: {factored}')
# x = -a를 대항식에 대입하면 0이어야 함
result = poly.subs(x, -a)
if result == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: poly({-a}) = {result}')