import sympy as sp

# 변수 정의
x = sp.Symbol('x')
C = sp.Symbol('C')

# 주어진 도함수
f_prime = 4*x**3 - 2*x

# 적분하여 f(x) 구하기
f_indefinite = sp.integrate(f_prime, x)
print(f'Indefinite integral: {f_indefinite}')

# 초기조건 f(0) = 3 적용
f_at_0 = f_indefinite.subs(x, 0)
print(f'f(0) = {f_at_0}, should be 3')

# C = 3이므로
f = x**4 - x**2 + 3

# 검증: f'(x)가 4x^3 - 2x와 같은지 확인
f_prime_check = sp.diff(f, x)
print(f'f\'(x) = {f_prime_check}')
print(f'Expected: {f_prime}')
print(f'Match: {sp.simplify(f_prime_check - f_prime) == 0}')

# 초기조건 검증
f_0 = f.subs(x, 0)
print(f'f(0) = {f_0}')
print(f'f(0) matches: {f_0 == 3}')

# f(2) 계산
f_2 = f.subs(x, 2)
print(f'f(2) = {f_2}')

if f_0 == 3 and sp.simplify(f_prime_check - f_prime) == 0 and f_2 == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')