from sympy import *

# 공차는 2
a = lambda n: 2*n - 1

# T_n = (3/2) * 8^(a_n)
T = lambda n: Rational(3, 2) * (8 ** a(n))

# 합 계산
total = sum(T(n) for n in range(1, 6))
expected = Rational(4, 21) * (2**30 - 1)

if total == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: computed {total}, expected {expected}')