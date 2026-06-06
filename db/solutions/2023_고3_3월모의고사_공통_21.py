import math

a = 4
k = 8

# 점들의 좌표
A = (1, k)
B = (k + math.log(k, a), k)
C = (k, 2 * math.log(k, a) + k)
D = (k, 1)

# AB와 CD의 길이
AB = B[0] - A[0]
CD = C[1] - D[1]

# 조건 1: AB × CD = 85
product = AB * CD
if abs(product - 85) < 1e-9:
    cond1_pass = True
else:
    cond1_pass = False

# 조건 2: 삼각형 CAD의 넓이 = 35
# 좌표를 이용한 삼각형 넓이 공식
area = 0.5 * abs(C[0] * (A[1] - D[1]) + A[0] * (D[1] - C[1]) + D[0] * (C[1] - A[1]))
if abs(area - 35) < 1e-9:
    cond2_pass = True
else:
    cond2_pass = False

if cond1_pass and cond2_pass:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')