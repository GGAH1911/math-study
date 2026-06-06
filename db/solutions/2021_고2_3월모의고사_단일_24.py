import math

# 2개의 e를 하나의 블록으로 취급
# 배열할 객체: (ee), c, h, r, u, p = 6개
# 6개 객체는 모두 서로 다르므로 6! 가지

answer = math.factorial(6)
print(f'e가 이웃하는 경우의 수: {answer}')

# 검증: 전체 배열의 수
total_arrangements = math.factorial(7) // math.factorial(2)  # e가 2개이므로 2!로 나눔
print(f'전체 배열의 수: {total_arrangements}')
print(f'e가 이웃하는 경우: {answer}')
print(f'e가 이웃하지 않는 경우: {total_arrangements - answer}')

if answer == 720:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')