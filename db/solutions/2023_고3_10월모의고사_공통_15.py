def verify():
    def compute_seq(a1):
        seq = [a1]
        for n in range(1, 5):
            an = seq[-1]
            if an % 4 == 0:
                seq.append(an // 2 + 2 * n)
            else:
                seq.append(an + 2 * n)
        return seq  # seq[0]=a1 ... seq[4]=a5

    valid = []
    for a1 in range(1, 5000):
        s = compute_seq(a1)
        a3, a4, a5 = s[2], s[3], s[4]
        if a3 > a5 and 50 < a4 + a5 < 60:
            valid.append(a1)

    if not valid:
        print('VERIFY_FAIL: no valid a1')
        return
    M = max(valid)
    m = min(valid)
    if M + m == 228:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: M={M}, m={m}, M+m={M+m}, valid={valid}')

verify()
