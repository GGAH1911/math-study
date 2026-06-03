# 직접 계산으로 검증
all_cases = 4**4  # 4개 문자, 4개 위치
a_never_appears = 3**4  # a를 제외한 3개 문자, 4개 위치
a_at_least_once = all_cases - a_never_appears

if a_at_least_once == 175:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')