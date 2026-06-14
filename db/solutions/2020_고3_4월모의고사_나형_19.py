from math import factorial
from collections import defaultdict

def multinomial_arrangements(items):
    if len(items) == 0:
        yield ()
        return
    counts = defaultdict(int)
    for x in items:
        counts[x] += 1
    for key in sorted(counts.keys()):
        counts[key] -= 1
        if counts[key] == 0:
            del counts[key]
        remaining = []
        for k, v in sorted(counts.items()):
            remaining.extend([k]*v)
        for rest in multinomial_arrangements(remaining):
            yield (key,) + rest
        counts[key] = counts.get(key, 0) + 1

def solve():
    # 이론값
    ga = factorial(9) // (factorial(2) * factorial(2) * factorial(5))  # 756
    na = factorial(6) // (factorial(2) * factorial(2) * factorial(2))  # 90

    # 완전탐색 검증 (week1 = (A=0,B=1,C=2) on days 0,1,2 고정 후 3! 곱)
    week1 = (0, 1, 2)
    items = [0]*2 + [1]*2 + [2]*5  # A x2, B x2, C x5

    total_rem = 0
    valid_rem = 0

    for perm in multinomial_arrangements(items):
        total_rem += 1
        valid = True
        for day in range(3):
            types_on_day = {week1[day]}
            for w in range(3):
                types_on_day.add(perm[w * 3 + day])
            if len(types_on_day) < 2:
                valid = False
                break
        if valid:
            valid_rem += 1

    # p = ga = 756, q = na = 90, p+q = 846
    p_plus_q = ga + na
    expected_valid_rem = ga - na  # 666

    if (total_rem == ga and valid_rem == expected_valid_rem and p_plus_q == 846):
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: ga={ga}(got {total_rem}), na={na}, valid_rem={valid_rem}(exp {expected_valid_rem}), p+q={p_plus_q}')

solve()
