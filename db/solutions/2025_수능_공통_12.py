import numpy as np

# a_n = (n+1)(2n-1)
def a_n(n):
    return (n + 1) * (2 * n - 1)

# b_n = 2n
def b_n(n):
    return 2 * n

# 원래 조건 검증: sum(a_k/b_{k+1}) = (1/2)n^2
for n in [1, 2, 3, 4, 5]:
    total = sum(a_n(k) / b_n(k + 1) for k in range(1, n + 1))
    expected = 0.5 * n**2
    assert abs(total - expected) < 1e-10, f"Failed for n={n}"

# 최종 답 계산
answer = sum(a_n(k) for k in range(1, 6))
assert answer == 120, f"Answer is {answer}, expected 120"

print('VERIFY_PASS')