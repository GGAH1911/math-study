import math

# 검증: r=8일 때 접선과 원이 만나는지 확인
# 원의 중심: (6, 8), 반지름: 8
# 접선: 3x - 4y = 25, 즉 3x - 4y - 25 = 0

# 중심 (6, 8)에서 직선까지의 거리
distance = abs(3*6 - 4*8 - 25) / math.sqrt(3**2 + 4**2)
print(f'Distance: {distance}')
print(f'Radius: 8')

r_answer = 8
if distance <= r_answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')