import sympy as sp
from sympy import sqrt, Rational

# 해 1: a=3, b=1/2, alpha=0, beta=10
a1, b1 = 3, Rational(1,2)
f1 = lambda x: Rational(1,4)*(x-4)**2 + a1
M1_calc = Rational(1,2) * (f1(0) + f1(10)) * (10 - 0)

# 해 2: a=8, b=-2+sqrt(5), alpha=-2*sqrt(5), beta=2*sqrt(5)
a2, b2 = 8, -2 + sqrt(5)
alpha2 = -2*sqrt(5)
beta2 = 2*sqrt(5)
f2 = lambda x: Rational(1,4)*(x-4)**2 + a2
f_alpha2 = f2(alpha2)
f_beta2 = f2(beta2)
M2_calc = Rational(1,2) * (f_alpha2 + f_beta2) * (beta2 - alpha2)
M2_simplified = sp.simplify(M2_calc)

# 결과 검증
print(f'M1 = {M1_calc}')
print(f'f_alpha2 = {sp.simplify(f_alpha2)}')
print(f'f_beta2 = {sp.simplify(f_beta2)}')
print(f'M2 simplified = {M2_simplified}')

M_max = max(M1_calc, M2_simplified)
m_min = min(M1_calc, M2_simplified)
M_plus_m = M_max + m_min
M_plus_m_simplified = sp.simplify(M_plus_m)

if M_plus_m_simplified == 95 + 68*sqrt(5):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')