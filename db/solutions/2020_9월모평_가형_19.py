import numpy as np

# 2020 9월모평 가형 19: OP=OY-OX → |OP|=|Y-X| = 점 X(단위 사분원호)와 Y(포물선) 사이 거리.
# X=(cosα,sinα), α∈[0,π/2];  Y=(s,(s-2)^2+1), s∈[2,3].  M^2+m^2?  (보기 ①=16-2√5)
CANDIDATE = 16 - 2 * np.sqrt(5)
al = np.linspace(0, np.pi / 2, 800)
X = np.stack([np.cos(al), np.sin(al)], axis=1)
mind, maxd = np.inf, -np.inf
for s in np.linspace(2, 3, 800):
    Y = np.array([s, (s - 2) ** 2 + 1])
    d2 = (X[:, 0] - Y[0]) ** 2 + (X[:, 1] - Y[1]) ** 2
    mind = min(mind, d2.min())
    maxd = max(maxd, d2.max())
val = mind + maxd                          # m^2 + M^2
print('VERIFY_PASS' if abs(val - CANDIDATE) < 1e-2 else 'VERIFY_FAIL')
