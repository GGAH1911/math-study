from itertools import product
# 서로다른 꽃4 + 같은 초콜릿2 → 5명, 빈 학생 없음. 경우의수?
CANDIDATE = 960
choc = [(c0,c1,c2,c3,c4) for c0 in range(3) for c1 in range(3) for c2 in range(3)
        for c3 in range(3) for c4 in range(3) if c0+c1+c2+c3+c4 == 2]
count = 0
for fl in product(range(5), repeat=4):
    fc = [0]*5
    for x in fl: fc[x] += 1
    for ch in choc:
        if all(fc[i]+ch[i] >= 1 for i in range(5)):
            count += 1
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
