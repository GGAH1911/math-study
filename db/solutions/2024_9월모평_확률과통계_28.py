from fractions import Fraction
from itertools import combinations, product

# 주사위 6면: 3의 배수면 A, 아니면 B
A = [1,2,3]
B = [1,2,3,4]

# 한 번의 시행에서 결과로 기록되는 '차'의 분포 계산 (원래 문제 그대로 시뮬레이션)
single_dist = {}
for die in range(1,7):
    p_die = Fraction(1,6)
    bag = A if die % 3 == 0 else B
    pairs = list(combinations(bag, 2))
    p_pair = Fraction(1, len(pairs))
    for x,y in pairs:
        d = abs(x-y)
        single_dist[d] = single_dist.get(d, Fraction(0)) + p_die * p_pair

# 분포 합 = 1 확인
assert sum(single_dist.values()) == 1

# 시행 2회 후 평균이 2인 사건 = 차의 합이 4인 사건
target_mean = Fraction(2)
prob = Fraction(0)
for d1, p1 in single_dist.items():
    for d2, p2 in single_dist.items():
        if Fraction(d1 + d2, 2) == target_mean:
            prob += p1 * p2

expected = Fraction(19, 81)
print('VERIFY_PASS' if prob == expected else f'VERIFY_FAIL got {prob}')
