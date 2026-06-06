import numpy as np
from fractions import Fraction

# 원래 문제: 무한급수 sum_{n=1}^{inf} 2/(n(n+2))
# 답: 3/2

expected_answer = Fraction(3, 2)

# 부분합을 충분히 큰 N까지 계산
def partial_sum(N):
    total = Fraction(0)
    for n in range(1, N+1):
        total += Fraction(2, n*(n+2))
    return total

# N을 충분히 크게 해서 수렴하는지 확인
N_values = [100, 1000, 10000, 100000]
for N in N_values:
    s_n = partial_sum(N)
    error = abs(float(s_n) - float(expected_answer))
    if error > 1e-6:
        print(f'N={N}: S_N={float(s_n):.10f}, expected={float(expected_answer):.10f}, error={error:.2e}')

# 공식으로도 확인: S_N = 3/2 - 1/(N+1) - 1/(N+2)
N = 100000
s_n_formula = Fraction(3, 2) - Fraction(1, N+1) - Fraction(1, N+2)
s_n_computed = partial_sum(N)

if abs(float(s_n_formula) - float(s_n_computed)) < 1e-10:
    limit = Fraction(3, 2)
    if limit == expected_answer:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')