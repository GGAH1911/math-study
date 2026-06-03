import numpy as np

def verify_absolute_inequality():
    # 부등식 |x-2| <= 3 을 만족하는 정수 개수
    count = 0
    solutions = []
    
    # 범위 확인: -1 <= x <= 5 이므로 충분히 넓게 확인
    for x in range(-5, 10):
        if abs(x - 2) <= 3:
            count += 1
            solutions.append(x)
    
    # 예상 답: 7개 (-1, 0, 1, 2, 3, 4, 5)
    if count == 7 and solutions == [-1, 0, 1, 2, 3, 4, 5]:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify_absolute_inequality()