from itertools import permutations

def solve():
    # A=-1, B=-2, C=-3 (black), 1,2,3,4 (white)
    # Circle of 7 positions; fix A=-1 at position 0 to remove rotational symmetry
    n = 7
    count = 0

    def adj(i, j):
        return abs(i - j) == 1 or abs(i - j) == n - 1

    for perm in permutations([-2, -3, 1, 2, 3, 4]):
        arr = [-1] + list(perm)  # A at position 0, rest at 1-6

        ok = True
        # Condition (가): no two black dishes adjacent
        black_pos = [i for i in range(n) if arr[i] < 0]
        for i in range(len(black_pos)):
            for j in range(i+1, len(black_pos)):
                if adj(black_pos[i], black_pos[j]):
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue

        # Condition (나): odd whites {1,3} not adjacent, even whites {2,4} not adjacent
        pos_of = {arr[i]: i for i in range(n)}
        if adj(pos_of[1], pos_of[3]):
            continue
        if adj(pos_of[2], pos_of[4]):
            continue

        count += 1

    return count

result = solve()
print(f'Count: {result}')
if result == 96:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
