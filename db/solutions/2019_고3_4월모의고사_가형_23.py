import sympy as sp

CANDIDATE = 49

# 원함수 정의
x = sp.Symbol('x', positive=True)
f = x**3 + 4*sp.sqrt(x)

# 도함수 계산
f_prime = sp.diff(f, x)

# x=4에서 도함수 값 계산
f_prime_at_4 = f_prime.subs(x, 4)

# 검증
if f_prime_at_4 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')