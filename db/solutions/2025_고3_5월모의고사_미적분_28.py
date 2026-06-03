import numpy as np

a = 6 * np.pi
b = 3 * np.pi / 2

# 범위 확인
assert 0 < a < 7*np.pi and 0 < b < 7*np.pi

# 원래 함수 정의
def f(x):
    return np.sin(a + b * np.cos(x))

def f_prime(x):
    return -b * np.sin(x) * np.cos(a + b * np.cos(x))

# 조건 (가): f'(x) = b 의 해 존재 -> x=-pi/2 에서 확인
x_ga = -np.pi / 2
ga_ok = np.isclose(f_prime(x_ga), b, atol=1e-9)

# 조건 (나): lim_{x->0} (1/x)*sin(f(a)*(pi+x/4)) = b/a
f_a = f(a)  # 원래 f(a) 직접 계산
target = b / a  # = 1/4

# 수치 극한 (x 아주 작게)
x_vals = [1e-7, 1e-8, 1e-9]
lim_vals = [(1/x)*np.sin(f_a*(np.pi + x/4)) for x in x_vals]
na_ok = all(np.isclose(v, target, atol=1e-5) for v in lim_vals)

# 답 확인
answer_ok = np.isclose(a + b, 15*np.pi/2, atol=1e-9)

if ga_ok and na_ok and answer_ok:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: ga={ga_ok}, na={na_ok}, ans={answer_ok}')
    print(f'f_prime(-pi/2)={f_prime(x_ga):.6f}, b={b:.6f}')
    print(f'lim_numerical={lim_vals[0]:.6f}, b/a={target:.6f}')
    print(f'a+b={a+b:.6f}, 15pi/2={15*np.pi/2:.6f}')
