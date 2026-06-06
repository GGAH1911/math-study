import sympy as sp
from sympy import log, symbols, solve, simplify

# 정의
alpha_val = 3**(-3/4)
beta_val = 3**(1/4)
m_val = 3

# 조건 검증
# 1. alpha * beta^3 = 1
cond1 = alpha_val * (beta_val**3)
print(f'alpha*beta^3 = {cond1}, expected 1')
assert abs(cond1 - 1.0) < 1e-10

# 2. 3*alpha = beta
cond2 = 3 * alpha_val
print(f'3*alpha = {cond2:.6f}, beta = {beta_val:.6f}')
assert abs(cond2 - beta_val) < 1e-10

# 3. beta^4 = m
cond3 = beta_val**4
print(f'beta^4 = {cond3}, m = {m_val}')
assert abs(cond3 - m_val) < 1e-10

# 4. m = beta/alpha
cond4 = beta_val / alpha_val
print(f'beta/alpha = {cond4}, m = {m_val}')
assert abs(cond4 - m_val) < 1e-10

# 5. g(m) = -4*3^(1/4)/3
log_m_alpha = sp.log(3**(-3/4), 3)
print(f'log_m(alpha) = {log_m_alpha}')
g_m = beta_val / float(log_m_alpha)
print(f'g(m) = {g_m:.6f}')
g_m_exact = -4 * (3**(1/4)) / 3
print(f'g(m) exact = {g_m_exact:.6f}')
assert abs(g_m - g_m_exact) < 1e-10

# 최종 계산
p = 3
q = 3**(1/4)
r = -4 * (3**(1/4)) / 3

product = p * q * r
print(f'p*q*r = {product:.6f}')
print(f'p*q*r = -4*sqrt(3) = {-4 * (3**0.5):.6f}')

result = (product)**2
print(f'(p*q*r)^2 = {result:.1f}')
assert abs(result - 48.0) < 1e-9
print('VERIFY_PASS')