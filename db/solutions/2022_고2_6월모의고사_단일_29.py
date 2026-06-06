import math

# b=8일 때 검증 (k=3)
print('b=8 (k=3):')
count_8 = 0
for x1 in range(1, 101):
    x2 = x1 ** 1.5
    if x2 <= 100 and x2 == int(x2):
        log4_x1 = math.log(x1) / math.log(4)
        log8_x2 = math.log(int(x2)) / math.log(8)
        if abs(log4_x1 - log8_x2) < 1e-10:
            count_8 += 1
            print(f'  log_4({x1}) = log_8({int(x2)}) ✓')

print(f'Count for b=8: {count_8}')

# b=64일 때 검증 (k=6)
print('\nb=64 (k=6):')
count_64 = 0
for x1 in range(1, 101):
    x2 = x1 ** 3
    if x2 <= 100:
        log4_x1 = math.log(x1) / math.log(4)
        log64_x2 = math.log(x2) / math.log(64)
        if abs(log4_x1 - log64_x2) < 1e-10:
            count_64 += 1
            print(f'  log_4({x1}) = log_64({x2}) ✓')

print(f'Count for b=64: {count_64}')

# 최종 답
if count_8 == 4 and count_64 == 4:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')