import sympy as sp
from fractions import Fraction

# a_n = 1/((2n-1)(2n+1)) 검증
total = Fraction(0)
for n in range(1, 11):
    a_n = Fraction(1, (2*n-1)*(2*n+1))
    total += a_n

# 조건식 검증: sum_{k=1}^n 1/((2k-1)*a_k) = n^2 + 2n
for n in range(1, 11):
    condition_sum = Fraction(0)
    for k in range(1, n+1):
        a_k = Fraction(1, (2*k-1)*(2*k+1))
        condition_sum += Fraction(1, (2*k-1)*a_k)
    expected = n*n + 2*n
    assert condition_sum == expected, f'n={n}: {condition_sum} != {expected}'

assert total == Fraction(10, 21), f'Sum error: {total}'
print('VERIFY_PASS')