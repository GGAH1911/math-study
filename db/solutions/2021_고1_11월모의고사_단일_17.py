import numpy as np

# 원의 중심과 반지름
center = np.array([1, 10])
radius = 3

# 정수 넓이를 만드는 각 직선에 대해 교점 개수 계산
count = 0

# m이 정수일 때 직선: sqrt(3)*x + y = sqrt(3) + 2*m
# 원의 중심에서 이 직선까지의 거리: |5 - m|

for m in range(-5, 15):
    dist = abs(5 - m)
    
    # 교점 개수 세기
    if dist < radius - 1e-9:
        count += 2
    elif abs(dist - radius) < 1e-9:
        count += 1

# 정답이 12인지 확인
if count == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')