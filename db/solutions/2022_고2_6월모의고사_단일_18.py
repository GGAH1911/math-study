import numpy as np

def verify():
    n = 18  # 검증할 답
    target = n / 18  # sin(2*n*a) = n/18

    if target > 1:
        print('VERIFY_FAIL')
        return

    # 2*n*a = arcsin(n/18) or pi - arcsin(n/18)
    arcsin_val = np.arcsin(target)
    domain_upper = np.pi / (2 * n)
    passed = False

    for theta in [arcsin_val, np.pi - arcsin_val]:
        a = theta / (2 * n)
        if not (0 < a < domain_upper):
            continue
        m = n / (6 * a)
        if not (0 < m < 6 * n):
            continue
        # 교점 조건: 3*sin(2*n*a) == m*a
        if abs(3 * np.sin(2 * n * a) - m * a) > 1e-9:
            continue
        # 넓이 조건
        C = (np.pi / (2 * n), 0)
        Ax, Ay = a, m * a
        Bx, By = -a, -m * a
        area = 0.5 * abs(
            Ax * (By - C[1]) +
            Bx * (C[1] - Ay) +
            C[0] * (Ay - By)
        )
        if abs(area - np.pi / 12) < 1e-9:
            passed = True

    # n=19는 해 없음 확인
    if 19 / 18 > 1:
        pass  # n=19: sin 조건 불만족 확인됨

    print('VERIFY_PASS' if passed else 'VERIFY_FAIL')

verify()
