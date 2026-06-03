import numpy as np

k = 4
alpha = np.arcsin(1/3)

solutions = []
for n in range(k):
    x1 = (alpha + 2*n*np.pi) / k
    x2 = (np.pi - alpha + 2*n*np.pi) / k
    for x in (x1, x2):
        if 0 <= x < 2*np.pi:
            solutions.append(x)

# 검증 1: 모든 해가 sin(kx)=1/3 만족
all_satisfy = all(abs(np.sin(k * x) - 1/3) < 1e-10 for x in solutions)
# 검증 2: 해의 개수 = 8
count_ok = len(solutions) == 8
# 검증 3: 합 = 7π
sum_ok = abs(sum(solutions) - 7*np.pi) < 1e-9

if all_satisfy and count_ok and sum_ok:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: satisfy={all_satisfy}, count={len(solutions)}, sum={sum(solutions):.6f}, 7pi={7*np.pi:.6f}')
