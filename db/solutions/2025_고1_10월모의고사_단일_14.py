import math

# 원래 문제의 조건
A = (-3, 2)
B = (2, 6)

# 구한 답: P=(-2,0), Q=(-1,0)
p = -2
q = -1
P = (p, 0)
Q = (q, 0)

# PQ = 1 확인
PQ = math.sqrt((q-p)**2)
assert abs(PQ - 1) < 1e-9, f'PQ={PQ} != 1'

# p < q 확인
assert p < q, 'P_x must be less than Q_x'

# AP + QB 계산
AP = math.sqrt((P[0]-A[0])**2 + (P[1]-A[1])**2)
QB = math.sqrt((Q[0]-B[0])**2 + (Q[1]-B[1])**2)
result = AP + QB

# 4√5 확인
expected = 4*math.sqrt(5)

# 수치 최솟값 확인 (brute force)
min_val = float('inf')
best_p = None
for i in range(-10000, 10000):
    pp = i / 100.0
    qq = pp + 1
    ap = math.sqrt((pp+3)**2 + 4)
    qb = math.sqrt((qq-2)**2 + 36)
    val = ap + qb
    if val < min_val:
        min_val = val
        best_p = pp

if abs(result - expected) < 1e-6 and abs(result - min_val) < 1e-4:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: AP+QB={result}, expected={expected}, brute_min={min_val} at p={best_p}')
