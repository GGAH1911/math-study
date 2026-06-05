import sympy as sp

def count_f_equals(m):
    n = 0
    if m > 0 and m <= 4:
        n += 1
    if m < 4:
        n += 1
    return n

def num_meet(k, c):
    if c == 0:
        return count_f_equals(k)
    return count_f_equals(k + c) + count_f_equals(k - c)

def has_valid_p(k):
    boundaries = set()
    for tp in [4 - k, k, (4 - k) / 2, k / 2]:
        if tp > 0:
            boundaries.add(tp)
    test_points = list(boundaries)
    delta = sp.Rational(1, 10**8)
    for b in list(boundaries):
        test_points.append(b - delta)
        test_points.append(b + delta)
    sb = sorted(boundaries)
    if sb:
        test_points.append(sb[0] / 2)
        for i in range(len(sb) - 1):
            test_points.append((sb[i] + sb[i+1]) / 2)
        test_points.append(sb[-1] + 1)
    for p in test_points:
        if p <= 0:
            continue
        if num_meet(k, p) == 3 and num_meet(k, 2*p) == 2:
            return True
    return False

alpha = sp.Rational(4, 3)
beta = sp.Rational(8, 3)
gamma = sp.Integer(4)

test_cases = [
    (sp.Rational(1, 100), True),
    (sp.Rational(1, 2), True),
    (sp.Rational(1), True),
    (alpha, True),
    (alpha + sp.Rational(1, 100), False),
    (sp.Rational(3, 2), False),
    (sp.Rational(2), False),
    (sp.Rational(5, 2), False),
    (beta, False),
    (beta + sp.Rational(1, 100), True),
    (sp.Rational(3), True),
    (sp.Rational(7, 2), True),
    (gamma - sp.Rational(1, 100), True),
    (gamma, False),
    (sp.Rational(5), False),
]

all_pass = True
for k, expected in test_cases:
    actual = has_valid_p(k)
    if actual != expected:
        all_pass = False
        print(f'FAIL k={k}: expected {expected}, got {actual}')

answer = alpha + beta + gamma
if all_pass and answer == 8:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: answer={answer}, all_pass={all_pass}')
