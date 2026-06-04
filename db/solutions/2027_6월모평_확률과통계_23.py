from math import factorial

# 4개의 문자 x, y, z, z 를 일렬로 나열
# z가 2번 반복 -> 같은 것이 있는 순열
result = factorial(4) // factorial(2)
expected = 12

if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')