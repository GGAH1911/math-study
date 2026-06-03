# P와 Q의 최종 위치 검증
a = 16  # 앞면 횟수
b = 30 - a  # 뒷면 횟수

# P의 위치: 앞면이 나올 때마다 +2
P = 2 * a

# Q의 위치: 뒷면이 나올 때마다 -1
Q = -1 * b

# 거리 계산
distance = abs(P - Q)

if distance == 46:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')