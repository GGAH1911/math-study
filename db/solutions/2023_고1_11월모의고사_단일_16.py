from sympy import symbols, simplify, solve
import sympy as sp

a = 5

# 점들의 좌표
A = (a + 1, 0)
B = (0, -4/a - 4)
C = (a, -4)
O = (0, 0)

# 신발끈 공식으로 사각형 OBCA의 넓이 계산
vertices = [O, B, C, A]
n = len(vertices)
area = 0
for i in range(n):
    x1, y1 = vertices[i]
    x2, y2 = vertices[(i + 1) % n]
    area += x1 * y2 - x2 * y1
area = abs(area) / 2

if area == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')