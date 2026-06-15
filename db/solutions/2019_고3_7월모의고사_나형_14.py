from fractions import Fraction
from sympy import symbols, simplify, summation

# 등차수열 a_n = d(n+3) 확인
d = 1  # 공차의 구체적 값으로 d=1 설정해도 무방 (비율만 중요)
def a(n):
    return d * (n + 3)

# 조건 확인: a_9 = 2*a_3
assert a(9) == 2 * a(3), f'a_9={a(9)}, 2*a_3={2*a(3)}'

# 합 계산
total = Fraction(0)
for n in range(1, 25):
    numerator = (a(n+1) - a(n))**2
    denominator = a(n) * a(n+1)
    total += Fraction(numerator, denominator)

# 망원급수 직접 계산으로 검증
telescope_sum = Fraction(1, 4) - Fraction(1, 28)
assert total == telescope_sum, f'total={total}, telescope={telescope_sum}'
assert total == Fraction(3, 14), f'Expected 3/14, got {total}'

print('VERIFY_PASS')