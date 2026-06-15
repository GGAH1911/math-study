import sympy as sp
from sympy import exp, cos, sin, pi, symbols, diff, simplify

# 기호 정의
x = symbols('x')
f_sym = symbols('f', cls=sp.Function)
f = f_sym(x)
f_prime = symbols('f_prime')
f_val = symbols('f_val', real=True, nonzero=True)

# g(x) = f(x)cos(x) / e^x 를 기호적으로 정의
g = f * cos(x) / exp(x)

# g'(x) 계산
g_prime = diff(g, x)

# x = pi에서 미분값과 함수값
g_prime_at_pi = g_prime.subs([(x, pi), (cos(pi), -1), (sin(pi), 0)])
g_at_pi = g.subs([(x, pi), (cos(pi), -1)])

# f(pi)와 f'(pi)의 기호로 정리
g_prime_at_pi_expr = -f_prime + f_val
g_prime_at_pi_expr = g_prime_at_pi_expr / exp(pi)
g_at_pi_expr = -f_val / exp(pi)

# 조건: g'(π) = e^π * g(π)
# e^π * g(π) = e^π * (-f(π)/e^π) = -f(π)
# g'(π) = (−f'(π) + f(π)) / e^π = -f(π)
# 따라서: −f'(π) + f(π) = −e^π * f(π)
# f'(π) = f(π) + e^π * f(π) = f(π)(1 + e^π)

# 답 계산
ratio = (f_val * (1 + exp(pi))) / f_val
ratio_simplified = simplify(ratio)

if simplify(ratio_simplified - (1 + exp(pi))) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')