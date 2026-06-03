from itertools import product

count = 0
for f in product([1, 2, 4], repeat=9):
    # 조건 (가): 원상 크기
    if f.count(1) != 3 or f.count(2) != 2 or f.count(4) != 4:
        continue
    # 조건 (나): x=1..7에 대해 f(x)+f(x+1) != f(x+2)
    ok = all(f[x-1] + f[x] != f[x+1] for x in range(1, 8))
    if ok:
        count += 1

print('VERIFY_PASS' if count == 930 else f'VERIFY_FAIL: got {count}')