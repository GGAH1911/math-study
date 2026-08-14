from itertools import permutations

count = 0
for perm in permutations([2, 3, 4, 5, 6, 7]):
    arr = [1] + list(perm)
    female_count = 0
    for i in range(7):
        if arr[i] in [5, 6, 7]:
            left = arr[(i - 1) % 7]
            right = arr[(i + 1) % 7]
            if left in [1, 2, 3, 4] and right in [1, 2, 3, 4]:
                female_count += 1
    if female_count == 1:
        count += 1

if count == 432:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')