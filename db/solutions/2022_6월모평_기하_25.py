import numpy as np

# 원의 중심 A(1,2), 반지름 r = |AB|
A = np.array([1.0, 2.0])
B = np.array([-3.0, 5.0])
AB_len = np.linalg.norm(B - A)  # 5.0

# P가 원 위의 점들: 둘레 = 2*pi*r
circumference = 2 * np.pi * AB_len  # 10*pi

# 검증: 원 위의 임의의 점이 조건을 만족하는지
thetas = np.linspace(0, 2*np.pi, 1000, endpoint=False)
for t in thetas:
    P = A + AB_len * np.array([np.cos(t), np.sin(t)])
    OP = P
    OA = A
    lhs = np.linalg.norm(OP - OA)
    rhs = AB_len
    if not np.isclose(lhs, rhs, atol=1e-9):
        print('VERIFY_FAIL')
        break
else:
    # 둘레가 10*pi와 일치하는지
    if np.isclose(circumference, 10 * np.pi, atol=1e-9):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
