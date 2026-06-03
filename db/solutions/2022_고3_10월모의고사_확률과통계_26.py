from itertools import permutations

count = 0
valid_tuples = []

# (4,2,1,1)의 모든 순열
for perm in set(permutations([4, 2, 1, 1])):
    a, b, c, d = perm
    if a * b * c * d == 8 and a + b + c + d < 10:
        count += 1
        valid_tuples.append(perm)

# (2,2,2,1)의 모든 순열
for perm in set(permutations([2, 2, 2, 1])):
    a, b, c, d = perm
    if a * b * c * d == 8 and a + b + c + d < 10:
        count += 1
        valid_tuples.append(perm)

# (8,1,1,1)의 모든 순열 (불만족 확인)
for perm in set(permutations([8, 1, 1, 1])):
    a, b, c, d = perm
    if a * b * c * d == 8 and a + b + c + d < 10:
        count += 1

if count == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')