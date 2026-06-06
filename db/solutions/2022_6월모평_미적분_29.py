import sympy as sp
from sympy import ln, exp, symbols, diff, simplify

t, x, k = symbols('t x k', positive=True, real=True)
a = exp(4) / 2

# 관계식 확인: ln(k) = k^2/t
# g(a) = e^2이므로 a에서: ln(e^2) = (e^2)^2 / a
check1 = ln(exp(2)) - (exp(4)) / a
print(f'ln(e^2) - e^4/a = {simplify(check1)} (0이어야 함)')

# g'(a) 계산
# g'(t) = -g(t)^3 / (t(t - 2g(t)^2))
g_a = exp(2)
t_a = a
derivative = -g_a**3 / (t_a * (t_a - 2 * g_a**2))
derivative_simplified = simplify(derivative)
print(f'g\'(a) = {derivative_simplified}')

# a × {g'(a)}^2 계산
result = a * derivative_simplified**2
result_simplified = simplify(result)
print(f'a × {{g\'(a)}}^2 = {result_simplified}')

# 분수 형태 확인
from sympy import nsimplify
fraction = nsimplify(result_simplified)
print(f'분수 형태: {fraction}')

# p + q 계산
if str(fraction) == '8/9':
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')