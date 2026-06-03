import numpy as np

def f(x):
    # 원래 그래프에 정의된 함수 (텐트 함수 + 이산 점)
    arr = np.asarray(x, dtype=float)
    result = np.zeros_like(arr)
    # -1 < x < 0: 상승 구간
    mask1 = (arr > -1) & (arr < 0)
    result[mask1] = arr[mask1] + 2
    # 0 < x < 1: 하강 구간
    mask2 = (arr > 0) & (arr < 1)
    result[mask2] = -arr[mask2] + 2
    # 이산 점
    result[arr == -1] = 2
    result[arr == 0] = 3
    result[arr == 1] = 1
    return result

eps = 1e-9
# lim_{x->0+} f(x)
xs_0plus = np.array([eps, eps/10, eps/100])
lim_0plus = np.mean(f(xs_0plus))  # 모두 약 2

# lim_{x->1-} f(x)
xs_1minus = np.array([1-eps, 1-eps/10, 1-eps/100])
lim_1minus = np.mean(f(xs_1minus))  # 모두 약 1

total = lim_0plus + lim_1minus
expected = 3

if abs(total - expected) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {total}, expected {expected}')
