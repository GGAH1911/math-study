# 세 문자 a, b, c 중에서 중복을 허락하여 4개를 택해 일렬로 나열
# 각 자리마다 3가지 선택 가능 -> 3^4
result = 3**4
expected = 81
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')