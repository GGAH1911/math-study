# 전체 의자: 1(R), 2(S), 3(R), 4(S), 5(R), 6(S)
# 학생: A₁,A₂ (1학년), B₁,B₂ (2학년), C₁,C₂ (3학년)
from itertools import permutations

count = 0
students = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
seats = [1, 2, 3, 4, 5, 6]
square_seats = [2, 4, 6]  # 사각 의자

# 전체 배치
for perm in permutations(students):
    # perm[i]는 seat[i]에 앉은 학생
    
    # 조건 (가): B는 사각 의자에만
    valid = True
    for student_idx, student in enumerate(perm):
        if student.startswith('B') and (student_idx + 1) not in square_seats:
            valid = False
            break
    
    if not valid:
        continue
    
    # 조건 (나): 같은 학년끼리 인접하지 않음
    for i in range(5):  # 인접 위치 쌍 검사
        s1, s2 = perm[i], perm[i+1]
        if s1[0] == s2[0]:  # 같은 학년
            valid = False
            break
    
    if valid:
        count += 1

if count == 64:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected: 64, Got: {count}')