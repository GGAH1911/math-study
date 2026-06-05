import numpy as np

# V자 왼쪽 팔: (-2,2)->(0,0), 기울기 -1 → f(x) = -x
def f_left(x):
    return -x

# V자 오른쪽 팔: (0,0)->(2,3), 기울기 3/2 → f(x) = 1.5*x
def f_right(x):
    return 1.5 * x

eps = 1e-9

# x→-2+ 극한: 왼쪽 팔에서 접근
lim1 = f_left(-2 + eps)   # → 2

# x→2- 극한: 오른쪽 팔에서 접근
lim2 = f_right(2 - eps)   # → 3

total = lim1 + lim2

if abs(lim1 - 2.0) < 1e-6 and abs(lim2 - 3.0) < 1e-6 and abs(total - 5.0) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: lim1={lim1}, lim2={lim2}, total={total}')
