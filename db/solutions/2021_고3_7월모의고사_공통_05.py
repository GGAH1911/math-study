import math

# 원래 부등식 검증: 5^(2x-7) <= (1/5)^(x-2)
# 답: x의 개수가 3
# 자연수 x가 1, 2, 3을 만족하는지 확인

count = 0
valid_x = []

# 자연수 범위에서 검증 (충분히 큰 범위)
for x in range(1, 10):
    left = 5**(2*x - 7)
    right = (1/5)**(x - 2)
    
    # 부등식 만족 여부
    if left <= right + 1e-10:  # 부동소수점 오차 허용
        count += 1
        valid_x.append(x)

if count == 3 and valid_x == [1, 2, 3]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'count: {count}, valid_x: {valid_x}')