from itertools import permutations
cards = (0,0,0,1,1,2,2)
seen = set()
for p in permutations(cards):
    if p in seen:
        continue
    seen.add(p)
count = 0
seen2 = set()
for p in permutations(cards):
    if p in seen2:
        continue
    seen2.add(p)
    ok = True
    for i in range(len(p)-1):
        if p[i]*p[i+1] > 1:
            ok = False
            break
    if ok:
        count += 1
print('VERIFY_PASS' if count == 18 else f'VERIFY_FAIL count={count}')
