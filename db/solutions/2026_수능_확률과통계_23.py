import itertools

# 네 문자 중 중복을 허락하여 3개를 택해 일렬로 나열
letters = ['a', 'b', 'c', 'd']

# 중복순열: product 사용
result = list(itertools.product(letters, repeat=3))
count = len(result)

if count == 64:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')