from itertools import combinations

white = [1,2,3,4]
black = [3,4,5,6]

total = 0
same_num = 0
black_2_same = 0

for wc in range(5):
    bc = 4 - wc
    for w_comb in combinations(white, wc):
        for b_comb in combinations(black, bc):
            nums = list(w_comb) + list(b_comb)
            if len(nums) != len(set(nums)):
                same_num += 1
                if bc == 2:
                    black_2_same += 1

if black_2_same == 17 and same_num == 29:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')