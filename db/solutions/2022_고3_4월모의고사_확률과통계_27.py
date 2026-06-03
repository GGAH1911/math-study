from itertools import permutations

balls = ['A', 'B', 'B', 'C', 'D', 'D']
count = 0
seen = set()

for perm in permutations(balls):
    if perm in seen:
        continue
    seen.add(perm)
    # perm[i] = box (i+1)에 들어가는 공
    # 조건 (가): 상자 1 (index 0)에 A 또는 B
    if perm[0] not in ('A', 'B'):
        continue
    # 조건 (나): 적어도 하나의 B-상자번호 < C-상자번호
    b_boxes = [i + 1 for i in range(6) if perm[i] == 'B']
    c_box = next(i + 1 for i in range(6) if perm[i] == 'C')
    if any(b < c_box for b in b_boxes):
        count += 1

print('VERIFY_PASS' if count == 80 else f'VERIFY_FAIL (count={count})')