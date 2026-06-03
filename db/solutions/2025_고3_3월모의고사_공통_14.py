from sympy import symbols, factor, simplify

# 결정된 f(x)
def f(x): return x**4 - 4*x**3 - 2*x**2 + 13*x + 7
def fp(x): return 4*x**3 - 12*x**2 - 4*x + 13

# 기본 조건 확인
assert f(1) == 15, f'f(1)={f(1)} != 15'
assert fp(1) == 1, f'fp(1)={fp(1)} != 1'

# h_a(t) = (t-a)^2 * Q(t,a), Q의 판별식 = -8(a+1)(a-3)
def disc(a_val): return -8*(a_val+1)*(a_val-3)

# 경계값에서 disc=0
assert disc(-1) == 0, 'disc(-1) != 0'
assert disc(3) == 0, 'disc(3) != 0'
# (-1,3) 내부에서 disc > 0
assert disc(0) > 0, 'disc(0) not > 0'
assert disc(1) > 0, 'disc(1) not > 0'
# 외부에서 disc <= 0
assert disc(-2) <= 0, 'disc(-2) not <= 0'
assert disc(5) <= 0, 'disc(5) not <= 0'

# 원래 문제 식으로 h_a(t) >= 0 검증 (a=-1, a=3 경계)
import numpy as np
for a_val in [-1, 3]:
    ts = np.linspace(-10, 10, 2000)
    ha = f(ts) - f(a_val) - fp(a_val)*(ts - a_val)
    assert np.all(ha >= -1e-8), f'h_a(t) < 0 at a={a_val}'

# f(4) 검증
result = f(4)
if result == 27:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: f(4)={result}')