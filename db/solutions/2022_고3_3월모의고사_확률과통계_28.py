from itertools import product

# 사탕 5개 각각을 A(0), B(1), C(2) 중 하나에 배분하는 모든 경우 열거
count = 0
for dist in product([0, 1, 2], repeat=5):
    a_count = dist.count(0)
    b_count = dist.count(1)
    # 조건 (가): A >= 1, 조건 (나): B <= 2
    if a_count >= 1 and b_count <= 2:
        count += 1

if count == 176:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')