import math

# 양 끝에 B 고정, 중간 6개 위치에 A 3, B 1, C 2 배치
# 중복순열 계산: 6! / (3! * 1! * 2!)

numerator = math.factorial(6)
denominator = math.factorial(3) * math.factorial(1) * math.factorial(2)
result = numerator // denominator

if result == 60:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')