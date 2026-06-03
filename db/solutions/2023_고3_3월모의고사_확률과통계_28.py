from itertools import permutations, combinations

def solve():
    breads = [0, 1, 2, 3, 4]
    arrangements = []
    for i in range(4):  # plate i gets 2 breads
        for two_b in combinations(breads, 2):
            remaining = [b for b in breads if b not in two_b]
            for perm in permutations(remaining):
                plate_b = [None] * 4
                plate_b[i] = tuple(sorted(two_b))
                r = 0
                for j in range(4):
                    if j != i:
                        plate_b[j] = (perm[r],)
                        r += 1
                arrangements.append(tuple(plate_b))
    
    def canonical(arr):
        n = len(arr)
        return min(tuple(arr[(j+k) % n] for j in range(n)) for k in range(n))
    
    unique = set(canonical(a) for a in arrangements)
    
    total = 0
    for bread_arr in unique:
        bread_counts = [len(b) for b in bread_arr]
        candy_limits = [3 - bc for bc in bread_counts]
        candy_ways = 0
        for c0 in range(candy_limits[0]+1):
            for c1 in range(candy_limits[1]+1):
                for c2 in range(candy_limits[2]+1):
                    c3 = 5 - c0 - c1 - c2
                    if 0 <= c3 <= candy_limits[3]:
                        candy_ways += 1
        total += candy_ways
    return total

result = solve()
if result == 540:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}')
