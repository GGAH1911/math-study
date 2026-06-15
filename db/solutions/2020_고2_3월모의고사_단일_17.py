from itertools import product
# 2×3 격자(1 2 3 / 4 5 6), 4색. (가) c1=c6, (나) 변 공유 다른색. 경우의수? (③=96)
CANDIDATE = 96
adj = [(0,1),(1,2),(3,4),(4,5),(0,3),(1,4),(2,5)]   # 인접쌍 (0-index)
count = 0
for c in product(range(4), repeat=6):
    if c[0] != c[5]:
        continue
    if all(c[i] != c[j] for i, j in adj):
        count += 1
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
