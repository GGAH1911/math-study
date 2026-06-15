from fractions import Fraction
from itertools import combinations

# 2개 공 꺼내기
combos = list(combinations([1, 2, 3, 4], 2))

# 소수 판별
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# 각 조합별 합과 분류
prime_combos = [(a, b) for a, b in combos if is_prime(a + b)]
non_prime_combos = [(a, b) for a, b in combos if not is_prime(a + b)]

# 확률 계산
prob_prime = Fraction(len(prime_combos), len(combos))  # 2/3
prob_non_prime = Fraction(len(non_prime_combos), len(combos))  # 1/3

# 동전 던질 때 앞면 2번
prob_heads_2_given_prime = Fraction(1, 4)  # 2번 중 2번
prob_heads_2_given_non_prime = Fraction(3, 8)  # 3번 중 2번

# 전체 앞면 2번 확률
prob_heads_2 = prob_heads_2_given_prime * prob_prime + prob_heads_2_given_non_prime * prob_non_prime

# 베이즈 정리
prob_prime_given_heads_2 = (prob_heads_2_given_prime * prob_prime) / prob_heads_2

# 검증
expected = Fraction(4, 7)
if prob_prime_given_heads_2 == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {prob_prime_given_heads_2} != {expected}')