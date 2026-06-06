# 무게중심 검증
a = 2
b = -2

# 세 점의 좌표
A = (a, 3)
B = (-2, 5)
C = (3, b)

# 무게중심 계산
centroid_x = (A[0] + B[0] + C[0]) / 3
centroid_y = (A[1] + B[1] + C[1]) / 3

# 주어진 무게중심
given_centroid = (1, 2)

# 검증
if abs(centroid_x - given_centroid[0]) < 1e-9 and abs(centroid_y - given_centroid[1]) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')