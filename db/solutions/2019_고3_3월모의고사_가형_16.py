from itertools import combinations

U = {1, 2, 3, 4, 5}
count = 0

# A∪B의 모든 3원소 부분집합
for AuB in combinations(U, 3):
    AuB_set = set(AuB)
    # A∩B의 모든 1원소 부분집합
    for elem_intersection in AuB_set:
        AintB_set = {elem_intersection}
        # 남은 2개 원소의 모든 분배
        remaining = AuB_set - AintB_set
        remaining_list = list(remaining)
        # A-B, B-A의 모든 가능한 분배 (2^2=4가지)
        for i in range(4):
            A_minus_B = set()
            B_minus_A = set()
            for j, elem in enumerate(remaining_list):
                if (i >> j) & 1:
                    A_minus_B.add(elem)
                else:
                    B_minus_A.add(elem)
            A = AintB_set | A_minus_B
            B = AintB_set | B_minus_A
            # 조건 확인
            if len(A & B) == 1 and len(A | B) == 3:
                count += 1

if count == 120:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')