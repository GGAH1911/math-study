import sympy as sp
x = sp.Symbol('x')
# 주어진 도함수
f_prime = 9*x**2 - 8*x + 1
# 적분하여 f(x) 구하기
f = sp.integrate(f_prime, x)
# 초기조건 f(1) = 10을 이용하여 상수 결정
C = 10 - f.subs(x, 1)
f_complete = f + C
# f(1) = 10 확인
assert f_complete.subs(x, 1) == 10, 'f(1) != 10'
# f(2) 계산
f_2 = f_complete.subs(x, 2)
if f_2 == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')