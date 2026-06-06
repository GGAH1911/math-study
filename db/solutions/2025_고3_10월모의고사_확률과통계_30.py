from fractions import Fraction
from math import comb

# P(3의 배수), P(3의 배수 아님)
p_mult3 = Fraction(2, 6)
p_not_mult3 = Fraction(4, 6)

# P(A > B) 계산
p_a_greater_b = Fraction(0)
for k in range(5):
    if k < 4/3:  # A > B 조건
        p_k = comb(4, k) * (p_mult3 ** k) * (p_not_mult3 ** (4 - k))
        p_a_greater_b += p_k

# 곱수: {2, 4, 6}, 3의 배수인 곱수: {6}
p_6 = Fraction(1, 6)
p_even_not_mult3 = Fraction(2, 6)  # 2, 4

# P(4번 모두 곱수 ∩ A > B) 계산
p_all_even_and_a_greater_b = Fraction(0)
for k in range(5):
    if k < 4/3:  # A > B 조건
        # k번은 6, (4-k)번은 {2, 4}
        p_k = comb(4, k) * (p_6 ** k) * (p_even_not_mult3 ** (4 - k))
        p_all_even_and_a_greater_b += p_k

# 조건부 확률
p_cond = p_all_even_and_a_greater_b / p_a_greater_b

# 기약분수 확인
from math import gcd
g = gcd(p_cond.numerator, p_cond.denominator)
numerator = p_cond.numerator // g
denominator = p_cond.denominator // g

if numerator == 1 and denominator == 16:
    answer = numerator + denominator
    print(f'VERIFY_PASS')
else:
    print(f'VERIFY_FAIL')