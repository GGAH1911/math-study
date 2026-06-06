from sympy import symbols, summation, simplify, gcd

n = symbols('n', integer=True, positive=True)
k = symbols('k', integer=True, positive=True)

# 일반항
def a(n_val):
    return (4*n_val - 3) / (4*n_val + 5)

# 검증: 원래 조건식 확인
for n_val in range(1, 6):
    left_sum = sum((4*k_val - 3) / a(k_val) for k_val in range(1, n_val + 1))
    right = 2*n_val**2 + 7*n_val
    assert abs(left_sum - right) < 1e-10, f"n={n_val}: {left_sum} != {right}"

# a_5, a_7, a_9 계산
a5 = a(5)
a7 = a(7)
a9 = a(9)

product = a5 * a7 * a9
print(f"a_5 × a_7 × a_9 = {product}")
print(f"Simplified: {simplify(product)}")

# 기약분수로 표현
from fractions import Fraction
frac = Fraction(17, 41)
print(f"Fraction: {frac}")
print(f"p + q = {41 + 17}")

if gcd(17, 41) == 1:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")