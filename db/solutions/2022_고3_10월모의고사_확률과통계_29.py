from itertools import product

# 비감소 함수 f: {1,2,3,4} -> {1,2,3,4,5,6}
# 조건: (가) 비감소, (나) f(1)<=3, (다) f(3)<=f(1)+4

count = 0
for f1 in range(1, 7):
    for f2 in range(f1, 7):
        for f3 in range(f2, 7):
            for f4 in range(f3, 7):
                # 조건 검사
                if f1 <= 3 and f3 <= f1 + 4:
                    count += 1

if count == 105:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected 105, got {count}')