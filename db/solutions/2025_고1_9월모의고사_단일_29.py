from itertools import permutations

count = 0
for perm in permutations(range(1, 9), 6):
    a1, a2, a3, a4, a5, a6 = perm
    A = a1 * 100 + a2 * 10 + a3
    B = a4 * 10 + a5
    C = a6
    
    if (A + B + C) % 5 == 0 and (A - B - C) % 5 == 0:
        count += 1

if count == 720:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')