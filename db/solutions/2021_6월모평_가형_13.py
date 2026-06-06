from itertools import product

count_a = 0
count_b = 0
count_both = 0
count_union = 0

for a, b in product(range(1, 7), repeat=2):
    cond_a = abs(a - 3) + abs(b - 3) == 2
    cond_b = a == b
    
    if cond_a:
        count_a += 1
    if cond_b:
        count_b += 1
    if cond_a and cond_b:
        count_both += 1
    if cond_a or cond_b:
        count_union += 1

prob = count_union / 36
if abs(prob - 1/3) < 1e-9 and count_union == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')