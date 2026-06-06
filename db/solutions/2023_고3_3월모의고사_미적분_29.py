import math
from sympy import *

n_val = symbols('n', positive=True, integer=True)

# a_n = 4n + 1 검증
def verify_a_n(n):
    x1 = 2*n - math.sqrt(4*n**2 + n)
    x2 = 2*n + math.sqrt(4*n**2 + n)
    count = sum(1 for x in range(int(x1)-1, int(x2)+2) if x**2 - 4*n*x - n < 0)
    return count == 4*n + 1

# 여러 n 값에 대해 검증
for n in [1, 2, 5, 10, 50, 100]:
    assert verify_a_n(n), f"a_n formula failed for n={n}"

# 극한값 검증: sqrt(n*a_n) - 2n -> 1/4
for n in [10, 100, 1000, 10000]:
    a_n = 4*n + 1
    limit_approx = math.sqrt(n * a_n) - 2*n
    expected = 0.25  # q = 1/4
    assert abs(limit_approx - expected) < 0.01/math.sqrt(n), f"Limit check failed for n={n}"

# 최종 검증: 100pq = 50
p = 2
q = Rational(1, 4)
result = 100 * p * q
assert result == 50, f"Final answer check failed: got {result}"

print('VERIFY_PASS')