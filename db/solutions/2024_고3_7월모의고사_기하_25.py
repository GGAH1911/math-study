import numpy as np

# 원래 조건: (OP - OA) · OA = 0 => 직선 2x + y = 10
# B = (5, 0), C = (0, 10), O = (0, 0)

O = np.array([0.0, 0.0])
A = np.array([4.0, 2.0])

# B: x축과 교점 (y=0)
B = np.array([5.0, 0.0])
# C: y축과 교점 (x=0)
C = np.array([0.0, 10.0])

# B가 조건 만족하는지 확인
OP_B = B
cond_B = np.dot(OP_B - A, A)
assert abs(cond_B) < 1e-9, f'B fails condition: {cond_B}'

# C가 조건 만족하는지 확인
OP_C = C
cond_C = np.dot(OP_C - A, A)
assert abs(cond_C) < 1e-9, f'C fails condition: {cond_C}'

# 삼각형 OBC 넓이 (외적 절반)
area = 0.5 * abs((B[0]-O[0])*(C[1]-O[1]) - (C[0]-O[0])*(B[1]-O[1]))

if abs(area - 25) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: area={area}')
