import sympy as sp
import numpy as np

CANDIDATE = -8

# f(x) = 1/(e^x + 2) 정의
x = sp.Symbol('x')
f = 1 / (sp.exp(x) + 2)

# f'(x) 계산
f_prime = sp.diff(f, x)

# g'(1/4)를 구하기 위해 먼저 g(1/4) 구하기
# f(a) = 1/4인 a를 찾아야 함
# 1/(e^a + 2) = 1/4
# e^a + 2 = 4
# e^a = 2
# a = ln(2)

a = sp.ln(2)

# f'(ln(2)) 계산
f_prime_at_a = f_prime.subs(x, a)
f_prime_at_a_simplified = sp.simplify(f_prime_at_a)

# g'(1/4) = 1 / f'(g(1/4)) = 1 / f'(ln(2))
g_prime_at_quarter = 1 / f_prime_at_a_simplified
g_prime_at_quarter_simplified = sp.simplify(g_prime_at_quarter)

# 수치 계산으로 검증
g_prime_value = float(g_prime_at_quarter_simplified)

if abs(g_prime_value - CANDIDATE) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')