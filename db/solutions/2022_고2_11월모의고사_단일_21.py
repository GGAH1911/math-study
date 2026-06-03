def S(n, a1, d):
    return n * a1 + n * (n - 1) * d // 2

def verify():
    cases = [
        (42, -2, 18),   # Case A
        (110, -15, 7),  # Case B
    ]
    total_a1 = 0
    all_pass = True
    for a1, d, m in cases:
        if not (d < 0):
            print(f'VERIFY_FAIL: d={d} >= 0'); all_pass = False; continue
        a_m  = a1 + (m - 1) * d
        a_m2 = a1 + (m + 1) * d
        if abs(a_m) != 2 * abs(a_m2):
            print(f'VERIFY_FAIL: |a_m|={abs(a_m)} != 2|a_m+2|={2*abs(a_m2)}'); all_pass = False; continue
        Sm  = S(m,     a1, d)
        Sm1 = S(m + 1, a1, d)
        Sm2 = S(m + 2, a1, d)
        max_S = max(Sm, Sm1, Sm2)
        min_S = min(Sm, Sm1, Sm2)
        if max_S != 460 or min_S != 450:
            print(f'VERIFY_FAIL: max={max_S}, min={min_S}'); all_pass = False; continue
        total_a1 += a1
    if all_pass and total_a1 == 152:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: total_a1={total_a1}')

verify()