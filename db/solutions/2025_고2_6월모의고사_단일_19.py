def count_x_for_K(K):
    eps = 1e-12
    if K > 1 + eps or K < -1 - eps:
        return 0
    if abs(K - 1) < eps:
        return 2  # x = 0 and x = 2pi
    if abs(K + 1) < eps:
        return 1  # x = pi
    return 2

def num_roots(m, n):
    # 원식: |2^m cos x - 2^n|^2 - (2^5+2^4)|2^m cos x - 2^n| + 2^9 = 0
    # f = |2^m cos x - 2^n| 로 두면 f^2 - 48 f + 512 = 0, 즉 f = 16 또는 32.
    # 그러면 cos x = (2^n +/- c)/2^m for c in {16, 32}
    K_set = set()
    for c in (32, 16):
        for s in (+1, -1):
            K_set.add((2**n + s * c) / 2**m)
    return sum(count_x_for_K(K) for K in K_set)

# 모든 (m,n), 1<=m,n<=7 에 대해 6근이 되는 쌍 수집
valid = [(m, n) for m in range(1, 8) for n in range(1, 8) if num_roots(m, n) == 6]
expected = [(5, 1), (5, 2), (5, 3), (5, 4)]

# 추가로 직접 원래 식에 알려진 근을 대입해 통과 확인
import math
def eq_val(x, m, n):
    fx = abs(2**m * math.cos(x) - 2**n)
    return fx**2 - (2**5 + 2**4) * fx + 2**9

ok = True
for (m, n) in expected:
    # cos x = (2^n +/- c)/2^m 의 해 모음
    roots = []
    for c in (32, 16):
        for s in (+1, -1):
            K = (2**n + s * c) / 2**m
            if -1 <= K <= 1:
                if abs(K - 1) < 1e-12:
                    roots.extend([0.0, 2 * math.pi])
                elif abs(K + 1) < 1e-12:
                    roots.append(math.pi)
                else:
                    a = math.acos(K)
                    roots.extend([a, 2 * math.pi - a])
    # 중복 제거
    uniq = []
    for r in roots:
        if not any(abs(r - u) < 1e-9 for u in uniq):
            uniq.append(r)
    if len(uniq) != 6:
        ok = False
        break
    for r in uniq:
        if abs(eq_val(r, m, n)) > 1e-7:
            ok = False
            break

if sorted(valid) == expected and len(valid) == 4 and ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
