from sympy import symbols, diff, integrate

x = symbols('x')

# 원래 문제 조건
f_prime = 6*x**2 + 5

# f(x) 구하기
f = integrate(f_prime, x)
C = 3  # f(0) = 3 조건에서
f = f + C

# 검증: f'(x) = 6x^2 + 5인지 확인
f_prime_check = diff(f, x)
assert f_prime_check == f_prime, 'f\'(x) 미분 검증 실패'

# 검증: f(0) = 3인지 확인
f_at_0 = f.subs(x, 0)
assert f_at_0 == 3, 'f(0) = 3 검증 실패'

# f(1) 계산
f_at_1 = f.subs(x, 1)
print(f'f(1) = {f_at_1}')
assert f_at_1 == 10, 'f(1) 계산 오류'
print('VERIFY_PASS')