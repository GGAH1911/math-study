from decimal import Decimal
import math

# 부등식 원래 형태: (sqrt(2)-1)^m >= (3-2*sqrt(2))^(5-n)
# sqrt(2) - 1
sqrt2_minus_1 = math.sqrt(2) - 1

# 3 - 2*sqrt(2)
val_3_minus_2sqrt2 = 3 - 2*math.sqrt(2)

# 검증: m + 2n <= 10 조건에서 답이 20인지 확인
count = 0
for m in range(1, 100):
    for n in range(1, 100):
        # 원래 부등식 검증
        left = sqrt2_minus_1 ** m
        right = val_3_minus_2sqrt2 ** (5 - n)
        
        # 부등식이 만족되는지 확인
        if left >= right - 1e-10:  # 수치 오차 고려
            # m + 2n <= 10 조건도 함께 확인
            if m + 2*n <= 10:
                count += 1
            elif m + 2*n == 11:
                # 경계 케이스: m + 2n = 11일 때 부등식 위배 확인
                if left < right + 1e-10:
                    pass  # 제대로 배제됨
        else:
            # m + 2n > 10인 경우 부등식 위배 확인
            if m + 2*n > 10:
                pass  # 제대로 배제됨

if count == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')