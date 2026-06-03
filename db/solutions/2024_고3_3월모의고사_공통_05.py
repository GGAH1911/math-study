import sympy as sp

x = sp.Symbol('x')

# 원래 주어진 도함수
f_prime = x * (3*x + 2)

# f(x) 적분으로 구하기
f = sp.integrate(f_prime, x) + 4  # C=4를 대입

# f(1) = 6 검증
f_at_1 = f.subs(x, 1)
print(f'f(1) = {f_at_1}, expected 6: {f_at_1 == 6}')

# f(0) 계산
f_at_0 = f.subs(x, 0)
print(f'f(0) = {f_at_0}')

if f_at_1 == 6 and f_at_0 == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')