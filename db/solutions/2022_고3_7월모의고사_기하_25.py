import numpy as np

# 원래 조건 검증
# A(-2,0), B(3,3), O=원점
# (OP - OA)·(OP - 2OB) = 0
# 이를 만족하는 P의 자취: (x-2)^2 + (y-3)^2 = 25

# 1) 원 위의 점들이 원래 조건을 만족하는지 확인
def check_condition(x, y):
    # OA = (-2, 0), 2*OB = (6, 6)
    v1 = np.array([x - (-2), y - 0])  # OP - OA
    v2 = np.array([x - 6, y - 6])    # OP - 2OB
    return np.dot(v1, v2)

# 원 위의 점 100개 샘플링
theta = np.linspace(0, 2*np.pi, 1000, endpoint=False)
xs = 2 + 5*np.cos(theta)
ys = 3 + 5*np.sin(theta)

residuals = [check_condition(x, y) for x, y in zip(xs, ys)]
max_err = np.max(np.abs(residuals))

# 2) 원의 반지름 확인
radius = 5
circumference = 2 * np.pi * radius

# 3) 원 밖의 점은 조건 불만족
x_out, y_out = 10, 10
val_out = check_condition(x_out, y_out)

if max_err < 1e-8 and abs(circumference - 10*np.pi) < 1e-8 and abs(val_out) > 1:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: max_err={max_err}, circ={circumference}, val_out={val_out}')
