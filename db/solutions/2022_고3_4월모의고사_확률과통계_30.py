from itertools import combinations, permutations

# Verify the answer
count = 0

# Generate all possible functions f: {1,2,3,4,5} -> {1,2,3,4,5}
for f_vals in range(5**5):
    f = []
    temp = f_vals
    for _ in range(5):
        f.append((temp % 5) + 1)
        temp //= 5
    
    # Check condition (나): range has exactly 3 elements
    range_f = set(f)
    if len(range_f) != 3:
        continue
    
    # Check condition (가): sum is even
    total = sum(f)
    if total % 2 != 0:
        continue
    
    count += 1

if count == 720:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')