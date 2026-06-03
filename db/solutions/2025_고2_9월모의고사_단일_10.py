import numpy as np

def f(x):
    return np.sin(x / 2) + np.sqrt(3) / 2

# 원래 함수에 두 교점 역대입 검증
x1 = 8 * np.pi / 3
x2 = 10 * np.pi / 3

y1 = f(x1)
y2 = f(x2)

# 두 점이 x축 위에 있는지 확인
if abs(y1) < 1e-9 and abs(y2) < 1e-9:
    # 두 점의 거리 계산
    AB = abs(x2 - x1)
    expected = 2 * np.pi / 3
    if abs(AB - expected) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')
