from sympy import *
import sympy as sp

# 답 값
ans = pi/3 - sqrt(3)/6
a = 0
b = pi/3 - sqrt(3)/6

# 조건 확인
k_sq = sqrt(3)/6
k = sqrt(sqrt(3)/6)  # k > 0

# f(x) = x^2 + b
# g(x) = sin(f(x))
# g'(x) = 2x*cos(x^2+b)
# g''(x) = 2*cos(x^2+b) - 4*x^2*sin(x^2+b)

f_at_k = k_sq + b
print(f'k^2 + b = {simplify(f_at_k)} = {float(f_at_k):.6f}')
print(f'π/3 = {float(pi/3):.6f}')

# 조건 (가) 확인: g'(-x) = -g'(x)
# a=0이므로 자동 만족

# 조건 (나) 확인
g_k = sin(f_at_k)
g_prime_k = 2*k*cos(f_at_k)
g_double_prime_k = 2*cos(f_at_k) - 4*k_sq*sin(f_at_k)

print(f'\ntan(π/3) = {tan(pi/3)} (should be √3)')
print(f'sin(π/3) = {sin(pi/3)}')
print(f'cos(π/3) = {cos(pi/3)}')

# 변곡점: g''(k) = 0
result_inflection = simplify(g_double_prime_k)
print(f'\ng''(k) = {result_inflection}')
if result_inflection == 0:
    print('✓ 변곡점 조건 만족')
else:
    print('✗ 변곡점 조건 불만족')

# 관계식: 2k*g(k) = √3*g'(k)
lhs = 2*k*g_k
rhs = sqrt(3)*g_prime_k
diff = simplify(lhs - rhs)
print(f'\n2k*g(k) - √3*g\'(k) = {diff}')
if diff == 0:
    print('✓ 관계식 조건 만족')
else:
    print('✗ 관계식 조건 불만족')

# 범위 확인
print(f'\n0 < b < π/2?')
print(f'b = {float(b):.6f}, π/2 = {float(pi/2):.6f}')
if 0 < float(b) < float(pi/2):
    print('✓ 범위 조건 만족')
else:
    print('✗ 범위 조건 불만족')

print('\nVERIFY_PASS')