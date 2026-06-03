def verify():
    # P = [k-2, k+2], Q = [-1, 5]
    # cond1: p→~q 거짓 → P∩Q ≠ ∅
    # cond2: p→q 거짓  → P⊄Q
    valid_k = []
    for k in range(-100, 101):
        P_lo, P_hi = k - 2, k + 2
        Q_lo, Q_hi = -1, 5
        cond1 = (P_lo <= Q_hi) and (P_hi >= Q_lo)          # P∩Q ≠ ∅
        P_sub_Q = (P_lo >= Q_lo) and (P_hi <= Q_hi)         # P⊆Q
        cond2 = not P_sub_Q                                  # P⊄Q
        if cond1 and cond2:
            valid_k.append(k)
    total = sum(valid_k)
    print('Valid k:', valid_k)
    print('Sum:', total)
    if total == 16:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify()