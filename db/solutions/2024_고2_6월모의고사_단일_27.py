import sympy as sp
from sympy import log as ln, symbols, simplify

a = sp.Symbol('a', positive=True, real=True)
b = a**81
c = a**(sp.Rational(9,2))

# 조건 1 검증: log_a(b) = 81
log_a_b = ln(b) / ln(a)
print(f'log_a(b) = {simplify(log_a_b)}')
assert simplify(log_a_b - 81) == 0, 'Condition 1 failed'

# 조건 2 검증: log_c(sqrt(a)) = log_sqrt(b)(c)
lhs = ln(a**(sp.Rational(1,2))) / ln(c)
rhs = ln(c) / ln(b**(sp.Rational(1,2)))
lhs_simplified = simplify(lhs)
rhs_simplified = simplify(rhs)
print(f'log_c(sqrt(a)) = {lhs_simplified}')
print(f'log_sqrt(b)(c) = {rhs_simplified}')
assert simplify(lhs - rhs) == 0, 'Condition 2 failed'

# 최종 답: log_c(b)
log_c_b = ln(b) / ln(c)
result = simplify(log_c_b)
print(f'log_c(b) = {result}')
assert result == 18, f'Expected 18, got {result}'

print('VERIFY_PASS')