from itertools import permutations

CANDIDATE = 36

# 6명을 원탁에 앉히는 모든 경우
# 회전 동등성: 학생을 0~5로 인덱싱, 0번(또는 한 명 고정)으로 정규화
students = list(range(6))
count = 0

# 모든 배열 생성
for perm in permutations(students):
    # A=0, B=1, C=2로 맵핑 (학생 이름)
    # perm[i]는 위치 i의 학생
    pos = {s: i for i, s in enumerate(perm)}
    a_pos, b_pos, c_pos = pos[0], pos[1], pos[2]
    
    # 원탁에서 이웃 관계 (6개 위치)
    def are_neighbors(pos1, pos2):
        return abs(pos1 - pos2) == 1 or abs(pos1 - pos2) == 5
    
    # 조건 검증
    cond_a = are_neighbors(a_pos, b_pos)  # A와 B 이웃
    cond_b = not are_neighbors(b_pos, c_pos)  # B와 C 이웃하지 않음
    
    if cond_a and cond_b:
        count += 1

# 회전 동등성 처리: 모든 배열을 생성했으므로 6으로 나눔
count_normalized = count // 6

if count_normalized == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count_normalized}, expected {CANDIDATE}')