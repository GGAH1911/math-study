from itertools import permutations

odd_nums = {1, 3, 5, 7, 9}
even_nums = {2, 4, 6, 8}
all_nums = list(range(1, 10))

count_condition = 0
count_both_odd = 0

for perm in permutations(all_nums, 4):
    a, b, c, d = perm
    if (a * b + c + d) % 2 == 1:
        count_condition += 1
        if a in odd_nums and b in odd_nums:
            count_both_odd += 1

if count_condition > 0 and count_both_odd / count_condition == 3 / 13:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')