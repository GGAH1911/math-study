import numpy as np

# 마름모 OABC: b = a + c, |a|=|c|=6, |b|=4
a = np.array([6.0, 0.0])
cx = -28.0 / 6.0  # a·c = -28 이므로 6*cx = -28
cy = np.sqrt(36.0 - cx**2)
c = np.array([cx, cy])
b = a + c  # 평행사변형 조건

# 조건 확인
assert abs(np.linalg.norm(a) - 6) < 1e-9, '|a|!=6'
assert abs(np.linalg.norm(c) - 6) < 1e-9, '|c|!=6'
assert abs(np.linalg.norm(b) - 4) < 1e-9, '|b|!=4'

t = 2.0 / 7.0
v1 = b - c
v2 = b + t * c
dot = np.dot(v1, v2)

if abs(dot) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
