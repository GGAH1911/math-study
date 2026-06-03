import math

# 원래 부등식 확인
def verify_inequality(x):
    if x <= 1:
        return False
    lhs = math.log10(x - 1) + math.log10(x + 2)
    return lhs <= 1

# x = 2, 3이 해에 포함되는지 확인
x_values = [2, 3]
total = 0
for x in x_values:
    if verify_inequality(x):
        total += x
    else:
        print(f'VERIFY_FAIL')
        exit()

# x = 4는 해에 포함되지 않는지 확인
if verify_inequality(4):
    print('VERIFY_FAIL')
    exit()

# 최종 답 확인
if total == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')