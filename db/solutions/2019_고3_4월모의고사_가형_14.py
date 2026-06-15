from itertools import combinations

# A = {1,...,25}, 1과 2를 모두 포함하고 원소 개수가 홀수인 부분집합 수
rest = list(range(3, 26))  # 23개 원소
count = 0
for r in range(0, len(rest) + 1):
    size = 2 + r  # 1,2 포함
    if size % 2 == 1:  # 홀수 크기
        count += len(list(combinations(rest, r)))

expected = 2 ** 22
if count == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', count, expected)
