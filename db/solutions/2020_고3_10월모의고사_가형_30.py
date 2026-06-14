CANDIDATE = 25
import sympy as sp
import numpy as np

# 원래 함수·조건 재현
x = sp.Symbol('x')
k, c, a_v, b_v = 1, 0, -2, -2

f = k*(x+1)**2 + c
g = (a_v*x + b_v)*sp.exp(f)

# f(0)=f(-2), f(0)!=0
assert f.subs(x,0) == f.subs(x,-2), 'f(0)!=f(-2)'
assert f.subs(x,0) != 0, 'f(0)=0 위반'
assert k > 0 and a_v < 0

# b=a 조건
assert a_v == b_v

# ae^c = -2
ae_c = a_v * np.exp(c)
assert abs(ae_c - (-2)) < 1e-10, f'ae^c={ae_c}'

# 조건 (가): 모든 x에 대해 (x+1)^2*(ae^f(x)-(-2))>=0 확인
# ae^f(x)<=-2이므로 m=-2일 때 (x+1)^2*(ae^f(x)+2)<=0 성립 확인
for t in [0, 0.5, 1, 2, -0.5, -1.5, -3]:
    val = float((t+1)**2 * (a_v*np.exp(k*(t+1)**2+c) - (-2)))
    assert val <= 1e-10, f'조건 (가) 위반 at x={t}: {val}'

# 조건 (나): 두 적분이 (e-e^4)/k 와 같은지
I1 = float(sp.integrate(g, (x, 0, 1)))
expected = (np.e - np.e**4) / k
assert abs(I1 - expected) < 1e-6, f'I1={I1}, expected={expected}'

f0 = float(f.subs(x, 0))
lower = -2*f0
I2 = float(sp.integrate(g, (x, lower, 1)))
assert abs(I2 - expected) < 1e-6, f'I2={I2}, expected={expected}'

# f(ab) 검산
ab = a_v * b_v  # = 4
fab = int(f.subs(x, ab))  # (4+1)^2 = 25
assert fab == CANDIDATE, f'f(ab)={fab} != CANDIDATE={CANDIDATE}'

print('VERIFY_PASS')
