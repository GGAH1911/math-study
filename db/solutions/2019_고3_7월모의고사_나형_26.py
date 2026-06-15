CANDIDATE = 510

import sympy as sp
from sympy import symbols, simplify

# a_n = 2^n인지 확인
def a(n):
    return 2**n

# a_1 = 2 확인
assert a(1) == 2, "a_1 should be 2"

# a_{n+1} = 2*a_n 확인
for n in range(1, 9):
    assert a(n+1) == 2*a(n), f"Point {n}: a_{n+1} != 2*a_n"

# 이차방정식이 중근을 가지는지 확인
# a_n*x^2 - a_{n+1}*x + a_n = 0
for n in range(1, 9):
    an = a(n)
    an1 = a(n+1)
    # 판별식
    discriminant = an1**2 - 4*an*an
    assert discriminant == 0, f"Point {n}: discriminant is not 0"

# 합 계산
total = sum(a(k) for k in range(1, 9))
assert total == CANDIDATE, f"Sum mismatch: {total} != {CANDIDATE}"

print("VERIFY_PASS")