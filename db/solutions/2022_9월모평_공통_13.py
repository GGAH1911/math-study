def check(d):
    a1 = -45
    # (가)
    ok_a = False
    for m in range(1, 2000):
        am = a1 + (m-1)*d
        am3 = a1 + (m+2)*d
        if abs(am) == abs(am3):
            ok_a = True
            break
    if not ok_a:
        return False
    # (나): S_n > -100 for all natural n
    s = 0
    consecutive_pos_growth = 0
    for n in range(1, 200000):
        term = a1 + (n-1)*d
        s += term
        if s <= -100:
            return False
        if term > 0:
            consecutive_pos_growth += 1
            if consecutive_pos_growth > 50 and s > 1000:
                break
    return True

valid = [d for d in range(1, 200) if check(d)]
total = sum(valid)
print('valid d =', valid, 'sum =', total)
print('VERIFY_PASS' if total == 48 else 'VERIFY_FAIL')
