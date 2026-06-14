import sympy as sp

# 주어진 조건을 검증
# f(3) = 4, f'(3) = 2인 함수 예시
# f(x) = (x-3)^2 + 2(x-3) + 4 = x^2 - 4x + 7

x = sp.Symbol('x')
h = sp.Symbol('h')
f = x**2 - 4*x + 7

# f(3) 계산
f_at_3 = f.subs(x, 3)
print(f'f(3) = {f_at_3}')

# f'(3) 계산
f_prime = sp.diff(f, x)
f_prime_at_3 = f_prime.subs(x, 3)
print(f"f'(3) = {f_prime_at_3}")

# 주어진 극한 검증: lim(h->0) [f(3+h)-4] / 2h = 1
numerator = f.subs(x, 3+h) - 4
expression = numerator / (2*h)
limit_value = sp.limit(expression, h, 0)
print(f'lim(h->0) [f(3+h)-4]/(2h) = {limit_value}')

# 최종 답
result = f_at_3 + f_prime_at_3
print(f'f(3) + f\'(3) = {result}')

if limit_value == 1 and result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')