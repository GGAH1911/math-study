import math

count = 0
for n in range(1, 101):
    sqrt_n = math.sqrt(n)
    x1 = 2 - sqrt_n
    x2 = 2 + sqrt_n
    
    # 원래 식에 대입하여 교점 확인
    y1 = x1**2 - 4*x1 + 4
    y2 = x2**2 - 4*x2 + 4
    
    if abs(y1 - n) < 1e-10 and abs(y2 - n) < 1e-10:
        result = (abs(x1) + abs(x2)) / 2
        # 자연수 판정
        if abs(result - round(result)) < 1e-10 and round(result) > 0:
            count += 1

if count == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')