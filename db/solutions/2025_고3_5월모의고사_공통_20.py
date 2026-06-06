import math

t = 4/3
k = 1/2

# 원래 함수로 검증
f_k = math.sqrt(3) * math.sin(t * math.pi * k)
g_k = -3 * math.cos(t * math.pi * k)
target = 3 * k

# f(k)과 g(k)이 3k와 같은지 확인
if abs(f_k - target) < 1e-9 and abs(g_k - target) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: f(k)={f_k}, g(k)={g_k}, 3k={target}')