import math

# 원래 문제의 조건
A = (8, 6, 2)

# xy평면에 대한 대칭이동: z 좌표를 음수로
B = (A[0], A[1], -A[2])

# 선분 AB의 길이
distance = math.sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2 + (A[2] - B[2])**2)

# 정답 검증
if distance == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')