from itertools import permutations

# 주어진 숫자들
numbers = [1, 2, 2, 3, 3]

# 모든 고유한 배열 생성
unique_perms = set(permutations(numbers))

# 경우의 수
result = len(unique_perms)
answer = 30

if result == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')