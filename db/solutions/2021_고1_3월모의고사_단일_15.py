from itertools import permutations

count_gana = 0
count_nana = 0
count_daha = 0

for perm in permutations(range(5), 3):
    has_A = 0 in perm
    has_B = 1 in perm
    has_C = 2 in perm
    
    if has_A and (has_B or has_C):
        if has_B and has_C:
            count_gana += 1
        elif has_B:
            count_nana += 1
        elif has_C:
            count_daha += 1

total = count_gana + count_nana + count_daha
assert count_gana == 6, f'Expected 6, got {count_gana}'
assert count_nana == 12, f'Expected 12, got {count_nana}'
assert count_daha == 12, f'Expected 12, got {count_daha}'
assert total == 30, f'Expected 30, got {total}'
print('VERIFY_PASS')