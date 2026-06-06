from itertools import permutations

def verify_arrangement(arr):
    # arr: 위치 0~7에 배치된 사람 (0=A, 1=B, 2=M1, 3=M2, 4=C, 5=F1, 6=F2, 7=F3)
    # 조건 (가): A와 B 이웃
    pos_A = arr.index(0)
    pos_B = arr.index(1)
    if (pos_A + 1) % 8 != pos_B and (pos_B + 1) % 8 != pos_A:
        return False
    
    # 조건 (나): C의 양옆이 모두 남학생
    pos_C = arr.index(4)
    left = arr[(pos_C - 1) % 8]
    right = arr[(pos_C + 1) % 8]
    # 남학생: 0(A), 1(B), 2(M1), 3(M2)
    if left > 3 or right > 3:
        return False
    return True

count = 0
for perm in permutations(range(8)):
    if verify_arrangement(perm):
        count += 1

# 회전 동일 처리: 8로 나눔
count_rotational = count // 8
if count_rotational == 288:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected 288, got {count_rotational}')