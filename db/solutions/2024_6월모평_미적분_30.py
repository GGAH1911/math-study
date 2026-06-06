import sympy as sp
from fractions import Fraction

# 정의된 수열 검증
a = -12
r = sp.Rational(-1, 2)

# 조건 검증
# 조건 1: b_3 = -1 (a_3 <= -1 확인)
a_3 = a * r**2
assert a_3 <= -1, f"b_3 = -1 조건 실패: a_3 = {a_3}"
assert a_3 == -3, f"a_3 값 오류: {a_3}"

# 조건 2: sum(b_{2n-1}) = -3
# 홀수항: a_1=-12, a_3=-3 (둘다 <=−1이므로 b=-1), a_5=-3/4, a_7=-3/16, ... (모두 >−1이므로 b=항)
odd_sum = -1 - 1  # b_1, b_3
for n in range(3, 20):  # a_5 부터
    a_odd = a * r**(2*n - 2)
    if abs(a_odd) < 1:
        odd_sum += float(a_odd)
tail_odd = sum(float(a * r**(2*n-2)) for n in range(3, 50))
assert abs(odd_sum - (-3)) < 1e-10, f"홀수합 오류: {odd_sum}"

# 조건 3: sum(b_{2n}) = 8
# 짝수항: 모두 양수이므로 b = a
even_sum = sum(float(a * r**(2*n-1)) for n in range(1, 50))
assert abs(even_sum - 8) < 1e-10, f"짝수합 오류: {even_sum}"

# 최종 답: sum(|a_n|)
total = sum(float(abs(a * r**(n-1))) for n in range(1, 100))
expected = 12 * (1 / (1 - 0.5))
assert abs(total - expected) < 1e-10, f"최종합 오류: {total}"
assert abs(expected - 24) < 1e-10, f"답 오류: {expected}"

print("VERIFY_PASS")