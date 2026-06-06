def compute_sequence(k, memo=None):
    if memo is None:
        memo = {}
    if k in memo:
        return memo[k]
    if k == 1:
        return 1
    if k == 3:
        return 4
    
    if k % 2 == 0:
        n = k // 2
        result = compute_sequence(n, memo) + 1
    elif k % 4 == 1:
        n = (k - 1) // 4
        result = compute_sequence(n, memo) + 4
    else:  # k % 4 == 3 and k > 3
        n = (k - 3) // 4
        result = compute_sequence(n, memo) + 4
    
    memo[k] = result
    return result

memo = {}
count = 0
for k in range(1, 1000):
    if compute_sequence(k, memo) == 10:
        count += 1

if count == 32:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: found {count}, expected 32')