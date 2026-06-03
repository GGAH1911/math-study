import numpy as np

def bisect(f, a, b, n=120):
    for _ in range(n):
        m = (a + b) / 2
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2

# 교점 조건: q = 1/p, a = p^p, 범위: 1 < p < 2

# ㄱ: pq = p*(1/p) = 1
giyeok = True

# ㄴ: a=2 => p^p=2 의 해가 p > sqrt(2)인지 확인
p_a2 = bisect(lambda p: p*np.log(p) - np.log(2), 1.001, 1.999)
nyu = bool(p_a2 > np.sqrt(2))

# ㄷ: 모든 a in (1,4)에 대해 S(p) < (a+1)/(2a)
# S(p) = (p^2+1)/(2p^2), a = p^p
a_vals = np.linspace(1.001, 3.999, 300)
digeut = True
for a in a_vals:
    p = bisect(lambda x, a=a: x*np.log(x) - np.log(a), 1.0001, 1.9999)
    Sp = (p**2 + 1) / (2 * p**2)
    bound = (a + 1) / (2 * a)
    if Sp >= bound:
        digeut = False
        break

if giyeok and nyu and digeut:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: giyeok={giyeok}, nyu={nyu}, digeut={digeut}')
