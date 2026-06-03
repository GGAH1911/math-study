from itertools import product
X = [1,2,3,4,5,6]
count = 0
for f1,f2,f3,f4,f5,f6 in product(X, repeat=6):
    if (f3+f4) % 5 != 0: continue
    if not (f1 < f3 and f2 < f3): continue
    if not (f4 < f5 and f4 < f6): continue
    count += 1
print('VERIFY_PASS' if count == 414 else f'VERIFY_FAIL: got {count}')