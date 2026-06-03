import sympy as sp

# 우리의 답: p=2, q=3, r=131 (공비=3)
p, q, r = 2, 3, 131

# 원래 함수 정의
def b_n(n):
    return sp.Rational(1, 2) * 3**(n-1)

def a_n(n):
    return n * (3**(n-1) + 2)

# 원래 조건 검증: sum_{k=1}^{n} a_k/(b_k+1) = n^2 + n
for test_n in range(1, 6):
    lhs = sum(a_n(k) / (b_n(k) + 1) for k in range(1, test_n + 1))
    rhs = test_n**2 + test_n
    assert lhs == rhs, f"n={test_n}: {lhs} != {rhs}"

# (다) 값 검증: sum_{n=1}^{5} a_n/n
sum_value = sum(a_n(n) / n for n in range(1, 6))
assert sum_value == 131, f"Sum error: {sum_value} != 131"

# p+q+r 검증
result = p + q + r
assert result == 136, f"Final answer error: {result} != 136"

print('VERIFY_PASS')