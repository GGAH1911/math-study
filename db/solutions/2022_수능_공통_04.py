# 그래프 해석 기반 극한값 검증
# 왼쪽 직선의 극한 (점 (-1, 3) 열린 원)
left_limit = 3

# x=2에서의 극한 (수평선 y=1)
# 좌극한과 우극한이 모두 1
right_limit = 1

# 답
answer = left_limit + right_limit

if answer == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')