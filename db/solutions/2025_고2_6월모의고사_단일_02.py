import math
# 원래 식 계산
result = math.log(25/2, 5) + math.log(10, 5)
print(f'계산 결과: {result}')
print(f'3과의 차이: {abs(result - 3)}')
if abs(result - 3) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')