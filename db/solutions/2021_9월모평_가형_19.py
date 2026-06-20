from itertools import combinations
from fractions import Fraction

# X의 공집합이 아닌 부분집합
X = {1, 2, 3, 4}
subsets = [s for s in (frozenset(combo) for r in range(1, 5) for combo in combinations(X, r))]
print(f'Non-empty subsets: {len(subsets)}')

# A ⊊ B ⊊ C인 순서쌍의 개수
count_favorable = 0
for A in subsets:
    for B in subsets:
        if A < B:  # A ⊊ B
            for C in subsets:
                if B < C:  # B ⊊ C
                    count_favorable += 1

print(f'A ⊊ B ⊊ C cases: {count_favorable}')

# 전체 경우의 수 (순서쌍)
total = 15 * 14 * 13
print(f'Total ordered selections: {total}')

# 확률
prob = Fraction(count_favorable, total)
print(f'Probability: {prob}')

if prob == Fraction(2, 91):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')