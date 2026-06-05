import numpy as np

def f(x, k):
    """함수 f(x)의 정의"""
    c_pi = k / 6 * np.pi
    sin_c = np.sin(c_pi)
    if x <= c_pi:
        return np.sin(x)
    else:
        return 2 * sin_c - np.sin(x)

def count_intersections(k):
    """k에 대해 y=f(x)와 y=sin(k/6π)의 교점 개수"""
    c_pi = k / 6 * np.pi
    sin_c = np.sin(c_pi)
    
    # sin x = sin_c의 해를 [0, 2π]에서 구하기
    if abs(sin_c - 1.0) < 1e-10:
        solutions = [np.pi / 2]
    elif abs(sin_c) < 1e-10:
        solutions = [0, np.pi, 2 * np.pi]
    else:
        x1 = np.arcsin(sin_c)
        x2 = np.pi - x1
        solutions = [x1, x2]
    
    # 각 해에 대해 f(x) = sin_c인지 확인
    count = 0
    for x in solutions:
        if 0 <= x <= 2 * np.pi + 1e-10:
            fx = f(x, k)
            if abs(fx - sin_c) < 1e-9:
                count += 1
    
    return count

total = 0
for k in range(1, 6):
    a_k = count_intersections(k)
    total += a_k

if total == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')