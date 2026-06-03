from math import comb

# X의 분포: 4개 동전에서 앞면 개수
probs_X = {k: comb(4, k) / 16 for k in range(5)}

# Y의 분포 계산
probs_Y = {}
probs_Y[0] = probs_X[0]  # Y=0 when X=0
probs_Y[1] = probs_X[1]  # Y=1 when X=1
probs_Y[2] = sum(probs_X[k] for k in [2, 3, 4])  # Y=2 when X>=2

# E(Y) 계산
E_Y = sum(y * probs_Y[y] for y in probs_Y)

# 기댓값이 13/8인지 확인
expected = 13/8
if abs(E_Y - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')