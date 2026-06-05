import numpy as np

# f(x) = 1 - 3*(x+1)^11 / 4^11
# 조건: f(-1)=1(최댓값), f(3)=-2(최솟값), 순감소, 미분가능
# int_{-1}^3 f(x)dx = 4 - 3/4^11 * 4^12/12 = 4 - 1 = 3  (해석적으로 정확)

def f(x):
    return 1.0 - 3.0*(x + 1.0)**11 / 4.0**11

def f_inv(y):
    # f(x)=y 풀면: (x+1)^11 = (1-y)*4^11/3, x = 4*((1-y)/3)^(1/11) - 1
    return 4.0 * ((1.0 - y) / 3.0) ** (1.0 / 11.0) - 1.0

# 경계조건 확인
assert abs(f(-1) - 1.0) < 1e-10, f'f(-1)={f(-1)}'
assert abs(f(3) - (-2.0)) < 1e-10, f'f(3)={f(3)}'

# int_{-1}^3 f(x)dx 수치 계산
x_arr = np.linspace(-1.0, 3.0, 2_000_000)
try:
    int_f = np.trapezoid(f(x_arr), x_arr)
except AttributeError:
    int_f = np.trapz(f(x_arr), x_arr)
assert abs(int_f - 3.0) < 0.01, f'int f = {int_f}'

# int_{-2}^1 f^{-1}(y)dy 수치 계산 → 8이어야 함
y_arr = np.linspace(-2.0, 1.0, 2_000_000)
try:
    int_finv = np.trapezoid(f_inv(y_arr), y_arr)
except AttributeError:
    int_finv = np.trapz(f_inv(y_arr), y_arr)

if abs(int_f - 3.0) < 0.01 and abs(int_finv - 8.0) < 0.01:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: int_f={int_f:.6f}, int_finv={int_finv:.6f}')
