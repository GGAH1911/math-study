from itertools import permutations

def verify():
    balls = [1, 2, 3, 4, 5]
    total_C = 0
    total_CD = 0

    for perm in permutations(balls):
        a = perm  # a[0]=a_1, ..., a[4]=a_5

        # Find minimum k (1-indexed) satisfying a[k-1] <= k
        min_k = None
        for k in range(1, 6):
            if a[k-1] <= k:
                min_k = k
                break

        # Condition C: minimum k is exactly 3
        if min_k == 3:
            total_C += 1
            # Condition D: a1 + a2 == a4 + a5
            if a[0] + a[1] == a[3] + a[4]:
                total_CD += 1

    from fractions import Fraction
    prob = Fraction(total_CD, total_C)
    expected = Fraction(4, 19)

    if prob == expected:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: got {total_CD}/{total_C} = {prob}, expected {expected}')

verify()