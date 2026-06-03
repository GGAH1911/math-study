from itertools import permutations

def verify():
    year_1 = {0, 2, 3, 4}
    year_2 = {1, 5, 6, 7}
    
    count = 0
    other_students = [1, 2, 3, 4, 5, 6, 7]
    
    for perm in permutations(other_students):
        arrangement = [0] + list(perm)
        
        a_pos = 0
        b_pos = arrangement.index(1)
        
        if abs(a_pos - b_pos) not in [1, 7]:
            continue
        
        valid = True
        for i in range(8):
            if arrangement[i] in year_1:
                next_i = (i + 1) % 8
                if arrangement[next_i] in year_1:
                    valid = False
                    break
        
        if valid:
            count += 1
    
    if count == 72:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: got {count}')

verify()