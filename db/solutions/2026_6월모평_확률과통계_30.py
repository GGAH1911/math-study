from itertools import product

count = 0
for f1, f2, f3, f4, f5 in product(range(1, 6), repeat=5):
    if f2 % 2 == 0:
        continue
    if not (f2 + 3 >= f1 + 1):
        continue
    if not (f3 + 3 >= f2 + 2):
        continue
    if not (f4 + 3 >= f3 + 3):
        continue
    if not (f5 + 3 >= f4 + 4):
        continue
    count += 1

if count == 115:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')