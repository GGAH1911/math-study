from itertools import combinations

U = {1, 2, 3, 4, 5, 6}
count = 0

for union_elements in combinations(U, 5):
    union_set = set(union_elements)
    for i in range(2**5):
        A_set = set()
        B_set = set()
        for j, elem in enumerate(union_elements):
            if (i >> j) & 1:
                A_set.add(elem)
            else:
                B_set.add(elem)
        
        if len(A_set & B_set) == 0 and len(A_set | B_set) == 5:
            count += 1

if count == 192:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')