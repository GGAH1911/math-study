import sympy as sp
from sympy import symbols, Sum, oo, simplify

# 검증: a_n = (-1/4)^(n-1)
# b_n = -3 * (1/4)^(n-1)

# 검증 1: 첫 번째 조건
q = sp.Rational(1, 4)
term1 = -20 * q / (1 - q**2)
term2 = 21 * q / (1 - q**3)
sum_cond1 = term1 + term2
print(f'조건 1 검증: {sum_cond1} (0이어야 함)')
assert sum_cond1 == 0, 'VERIFY_FAIL'

# 검증 2: 급수 수렴
b1 = -3
d = sp.Rational(1, 4)
geometric_sum = b1 / (1 - d)
print(f'∑b_n = {geometric_sum}')
assert geometric_sum == -4, 'VERIFY_FAIL'

# 검증 3: 최종 답
answer = b1 * geometric_sum
print(f'b_1 × ∑b_n = {answer}')
assert answer == 12, 'VERIFY_FAIL'

print('VERIFY_PASS')