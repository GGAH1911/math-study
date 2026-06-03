def verify_k(k):
    a1 = k
    a2 = a1 - 2 - k if a1 > 0 else a1 + 2 - k
    a3 = a2 + 4 - k if a2 <= 0 else a2 - 4 - k
    a4 = a3 + 6 - k if a3 <= 0 else a3 - 6 - k
    a5 = a4 + 8 - k if a4 <= 0 else a4 - 8 - k
    a6 = a5 + 10 - k if a5 <= 0 else a5 - 10 - k
    return a3 * a4 * a5 * a6 < 0

valid_k = [k for k in range(1, 20) if verify_k(k)]
ans_sum = sum(valid_k)
if ans_sum == 14 and valid_k == [3, 5, 6]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')