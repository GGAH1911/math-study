import sympy as sp
from sympy import cos, sin, tan, pi, limit, symbols, simplify

x = symbols('x', real=True)
a = 1 - 3*pi/4
b = -a
alpha = -3*pi/4
beta = 3*pi/4

# 함수 정의
def f(t):
    return a*cos(t) + t*sin(t) + b

# 극한 c 계산
c = limit(f(x)/x**2, x, 0)
print(f'c = {c}')

# 조건 (가) 확인: f'(α) = f'(β) = 0
f_prime = (1-a)*sin(x) + x*cos(x)
f_prime_alpha = f_prime.subs(x, alpha)
f_prime_beta = f_prime.subs(x, beta)
print(f'f\'(α) = {simplify(f_prime_alpha)}')
print(f'f\'(β) = {simplify(f_prime_beta)}')

# 조건 (나) 확인
tan_alpha = tan(alpha)
tan_beta = tan(beta)
cond_na = (tan_beta - tan_alpha)/(beta - alpha) + 1/beta
print(f'조건(나) = {simplify(cond_na)}')

# 최종 계산: f(π/2) + c
angle = (beta - alpha)/3
f_angle = f(angle)
result = f_angle + c
result_simplified = simplify(result)
print(f'f((β-α)/3) + c = {result_simplified}')

# p + qπ 형식으로 분해
result_expanded = simplify(result)
coeff_const = simplify(result_expanded.coeff(pi, 0))
coeff_pi = simplify(result_expanded.coeff(pi, 1))
print(f'p = {coeff_const}, q = {coeff_pi}')

p = coeff_const
q = coeff_pi
answer = simplify(120*(p + q))
print(f'120*(p+q) = {answer}')

if answer == 135:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')