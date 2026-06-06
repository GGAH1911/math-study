import math

# 정의되는 정수 a의 개수 구하기
count = 0
valid_a = []

for a in range(-10, 10):
    # 조건 1: 밑 |a|가 양수이고 1이 아님
    if abs(a) == 0 or abs(a) == 1:
        continue
    
    # 조건 2: 진수가 양수
    argument = -a**2 - 4*a + 21
    if argument <= 0:
        continue
    
    # 로그가 정의됨
    count += 1
    valid_a.append(a)
    
    # 검증: 실제로 로그 계산 가능한지 확인
    base = abs(a)
    if base > 0 and base != 1 and argument > 0:
        log_value = math.log(argument) / math.log(base)

if count == 6 and valid_a == [-6, -5, -4, -3, -2, 2]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')