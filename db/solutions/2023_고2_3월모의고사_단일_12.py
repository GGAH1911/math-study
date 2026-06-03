from itertools import permutations, combinations

# 1학년 2명, 2학년 4명
students_grade1 = [1, 2]  # 1학년
students_grade2 = [3, 4, 5, 6]  # 2학년

count = 0

# 앞줄(위치 0, 1)에 배치할 2학년 2명 선택 및 배열
for front_perm in permutations(students_grade2, 2):
    # 뒷줄에 배치될 남은 학생들
    remaining_grade2 = [s for s in students_grade2 if s not in front_perm]
    
    # 뒷줄(위치 2, 3, 4, 5)에 1학년 2명과 남은 2학년 2명 배치
    all_back_students = students_grade1 + remaining_grade2
    
    for back_perm in permutations(all_back_students, 4):
        # 1학년 학생의 위치 찾기
        pos1 = back_perm.index(1)
        pos2 = back_perm.index(2)
        
        # 이웃하지 않는 조건 확인 (같은 줄에서 인접하지 않음)
        # 뒷줄 위치: 0, 1, 2, 3 (원래 위치 2, 3, 4, 5)
        if abs(pos1 - pos2) > 1:  # 바로 옆이 아님
            count += 1

print('VERIFY_PASS' if count == 144 else f'VERIFY_FAIL: {count}')