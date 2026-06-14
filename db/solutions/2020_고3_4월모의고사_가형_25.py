CANDIDATE = 96

from itertools import permutations

def solve():
    # A1을 위치 0에 고정하여 회전 대칭 제거
    # 나머지 6명(A2, B1, B2, C1, C2, C3)을 위치 1~6에 배치
    others = ['A2', 'B1', 'B2', 'C1', 'C2', 'C3']
    n = 7
    count = 0
    for perm in permutations(others):
        arrangement = ['A1'] + list(perm)
        # A1(pos=0)과 A2의 인접 여부 확인
        a2_pos = arrangement.index('A2')
        a1_pos = 0
        if not (abs(a1_pos - a2_pos) == 1 or abs(a1_pos - a2_pos) == n - 1):
            continue
        # B1과 B2의 인접 여부 확인
        b1_pos = arrangement.index('B1')
        b2_pos = arrangement.index('B2')
        if not (abs(b1_pos - b2_pos) == 1 or abs(b1_pos - b2_pos) == n - 1):
            continue
        count += 1
    return count

result = solve()
if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: computed={result}, candidate={CANDIDATE}')
