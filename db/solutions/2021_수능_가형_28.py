from sympy import symbols, solve, diff, simplify

CANDIDATE = 72

# 검증: a=0, b=5일 때
a, b = 0, 5

# f(x) = x(x-b)^2 정의
x = symbols('x', real=True)
f = x * (x - b)**2
f_prime = diff(f, x)

# f'(1) = 8 확인
f_prime_at_1 = f_prime.subs(x, 1)
print(f'f\'(1) = {f_prime_at_1}', 'VERIFY_PASS' if f_prime_at_1 == 8 else 'VERIFY_FAIL')

# g(x) = x³+x+1 정의
from sympy import symbols
t = symbols('t', real=True)
g = t**3 + t + 1

# g⁻¹(3) = 1 확인 (g(1)=3)
g_at_1 = g.subs(t, 1)
print(f'g(1) = {g_at_1}', 'verified' if g_at_1 == 3 else 'FAIL')

# g'(x) = 3x²+1
g_prime = diff(g, t)
g_prime_at_1 = g_prime.subs(t, 1)
print(f'g\'(1) = {g_prime_at_1}', 'verified' if g_prime_at_1 == 4 else 'FAIL')

# h'(3) = f'(1)/g'(1) = 8/4 = 2 확인
h_prime_at_3 = f_prime_at_1 / g_prime_at_1
print(f'h\'(3) = {h_prime_at_3}', 'verified' if h_prime_at_3 == 2 else 'FAIL')

# f(8) 계산
f_at_8 = f.subs(x, 8)
print(f'f(8) = {f_at_8}')
print('VERIFY_PASS' if f_at_8 == CANDIDATE else 'VERIFY_FAIL')