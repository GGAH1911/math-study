import numpy as np

def count_intersections(k_val, c):
    coeffs = [1, -6, 9, k_val - c]
    roots = np.roots(coeffs)
    real_roots = sorted([r.real for r in roots if abs(r.imag) < 1e-7])
    unique = []
    for r in real_roots:
        if not unique or abs(r - unique[-1]) > 1e-5:
            unique.append(r)
    return len(unique)

def sum_an(k_val):
    return sum(count_intersections(k_val, 3*n) for n in range(1, 5))

# k 값이 바뀔 때 a_n이 변하는 임계점만 검사하면 충분하지만, 안전을 위해 넓게 검사.
candidates = set()
for n in range(1, 5):
    candidates.add(3*n)
    candidates.add(3*n - 4)

valid = sorted(k for k in candidates if sum_an(k) == 7)
total = sum(valid)

# 경계 외 일반 k에서는 합이 7이 될 수 없음을 추가 확인
extra_ok = True
for i in range(-200, 300):
    k_test = i / 10.0
    if k_test in candidates:
        continue
    if sum_an(k_test) == 7:
        extra_ok = False
        break

if valid == [2, 3, 5, 6, 8, 9] and total == 33 and extra_ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
