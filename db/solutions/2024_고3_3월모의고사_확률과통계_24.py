# 숫자 1, 2, 3 중 중복 허용하여 4개를 택해 나열한 수가 홀수인 경우
from itertools import product

count = 0
for perm in product([1, 2, 3], repeat=4):
    # 4개 숫자로 만든 네 자리 수
    num = perm[0] * 1000 + perm[1] * 100 + perm[2] * 10 + perm[3]
    # 홀수 판정: 일의 자리(perm[3])가 홀수
    if num % 2 == 1:
        count += 1

if count == 54:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {count}')