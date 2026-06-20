from itertools import permutations

def are_neighbors_circular(arr, i, j):
    """원형 배열에서 위치 i와 j가 이웃하는지 확인"""
    n = len(arr)
    return (i - j) % n == 1 or (j - i) % n == 1

# 학생: (학년, 번호) 형태
students = [('1', 1), ('1', 2), ('2', 1), ('2', 2), ('3', 1), ('3', 2), ('3', 3)]

# 회전 고정: ('3', 1)을 위치 0에 고정
fixed = ('3', 1)
others = [s for s in students if s != fixed]

count = 0
for perm in permutations(others):
    arr = [fixed] + list(perm)
    
    # 1학년 학생의 위치
    a_pos = [i for i, s in enumerate(arr) if s[0] == '1']
    # 2학년 학생의 위치
    b_pos = [i for i, s in enumerate(arr) if s[0] == '2']
    
    # 1학년이 이웃하고, 2학년도 이웃하는지 확인
    if are_neighbors_circular(arr, a_pos[0], a_pos[1]):
        if are_neighbors_circular(arr, b_pos[0], b_pos[1]):
            count += 1

assert count == 96, f"Expected 96, got {count}"
print('VERIFY_PASS')