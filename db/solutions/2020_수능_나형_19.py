from itertools import permutations, combinations

def verify():
    count = 0
    
    # Case 1: 홀수 3개 각 1회, 짝수 1종류 2회
    for even in [2, 4, 6]:
        seq = [1, 3, 5, even, even]
        count += len(set(permutations(seq)))
    
    # Case 2: 홀수 1종류 1회, 짝수 2종류 각 2회
    for odd in [1, 3, 5]:
        for e1, e2 in combinations([2, 4, 6], 2):
            seq = [odd, e1, e1, e2, e2]
            count += len(set(permutations(seq)))
    
    answer = 450
    if count == answer:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: expected {answer}, got {count}')

verify()