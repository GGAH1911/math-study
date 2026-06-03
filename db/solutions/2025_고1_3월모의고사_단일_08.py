import math

# 일반적인 경우: 정삼각형으로 검증
# B = (0, 0), C = (12, 0), A = (6, 6√3)
a, b = 6, 6 * math.sqrt(3)
B = (0, 0)
C = (12, 0)
A = (a, b)

# 무게중심 G
G = ((A[0] + B[0] + C[0])/3, (A[1] + B[1] + C[1])/3)
print(f"G = {G}")

# G를 지나고 BC와 평행한 직선: y = G[1]
y_line = G[1]

# AC 위의 점 중 y = y_line인 점 D 찾기
# AC: A + t(C - A) for t in [0, 1]
# y좌표: A[1] + t(C[1] - A[1]) = y_line
if A[1] != C[1]:
    t = (y_line - A[1]) / (C[1] - A[1])
    D = (A[0] + t * (C[0] - A[0]), A[1] + t * (C[1] - A[1]))
else:
    D = None

print(f"D = {D}")
print(f"D's y-coordinate: {D[1]}, should equal G's y: {G[1]}")
print(f"y-coordinates match: {abs(D[1] - G[1]) < 1e-10}")

# GD의 길이
GD_length = abs(D[0] - G[0])
print(f"GD length = {GD_length}")
print(f"GD = 4? {abs(GD_length - 4) < 1e-10}")

if abs(GD_length - 4) < 1e-10:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")