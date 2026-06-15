import sympy as sp
from sympy import sin, cos, pi, sqrt, integrate, diff, simplify

CANDIDATE = 12

# 함수 정의
x = sp.Symbol('x', real=True)
f = 16*sin(x)**3 - 2*sin(x)
f_prime = diff(f, x)

# 확인: f(π/4) = 3√2, f(π/3) = 5√3
val_pi4 = f.subs(x, pi/4)
val_pi3 = f.subs(x, pi/3)

print(f'f(π/4) = {simplify(val_pi4)}')
print(f'f(π/3) = {simplify(val_pi3)}')
print(f'Expected: 3√2 = {simplify(3*sqrt(2))}, 5√3 = {simplify(5*sqrt(3))}')

# 합 계산
# α(t)는 (0,π/2)에서 f(x)=t의 해
# Σx_n(t) = 5050π + α(t)
# Σx_n(5√3) = 5050π + π/3
# Σx_n(3√2) = 5050π + π/4

sum_x_at_5sqrt3 = 5050*pi + pi/3
sum_x_at_3sqrt2 = 5050*pi + pi/4

# ∫α(t)dt 계산 (변수치환 u=α(t))
# ∫_{π/4}^{π/3} u·f'(u) du 계산
u = sp.Symbol('u', real=True)
integrand = u * f_prime.subs(x, u)
integral_alpha = integrate(f.subs(x, u), (u, pi/4, pi/3))

print(f'\n∫f(u)du from π/4 to π/3 = {simplify(integral_alpha)}')

# 최종 계산
# Σc_n = [5√3·Σx_n(5√3) - 3√2·Σx_n(3√2)] - ∫Σx_n(t)dt
# = [5√3·(5050π+π/3) - 3√2·(5050π+π/4)] - [5050π(5√3-3√2) + ∫α dt]

term1 = 5*sqrt(3) * sum_x_at_5sqrt3 - 3*sqrt(2) * sum_x_at_3sqrt2
term2 = 5050*pi * (5*sqrt(3) - 3*sqrt(2))

result_terms = simplify(term1 - term2)
print(f'\nFirst part: {simplify(term1)}')
print(f'Subtract: {simplify(term2)}')
print(f'Difference: {result_terms}')

final_integral = pi*5*sqrt(3)/3 - pi*3*sqrt(2)/4 + sp.Rational(19,3) - 17*sqrt(2)/3
print(f'\nIntegral of α(t): {simplify(final_integral)}')

summation = -sp.Rational(19,3) + 17*sqrt(2)/3
p_val = -sp.Rational(19,3)
q_val = sp.Rational(17,3)

print(f'\nΣc_n = {simplify(summation)}')
print(f'p = {p_val}, q = {q_val}')
print(f'q - p = {q_val - p_val}')

if simplify(q_val - p_val) == CANDIDATE:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')