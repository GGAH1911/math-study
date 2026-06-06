def verify():
    count = 0
    for d1 in [1, 2]:
        for d2 in [0, 1, 2]:
            for d3 in [0, 1, 2]:
                for d4 in [0, 1, 2]:
                    for d5 in [0, 1, 2]:
                        digits = [d1, d2, d3, d4, d5]
                        has_zero = 0 in digits
                        has_one = 1 in digits
                        if has_zero and has_one:
                            count += 1
    if count == 115:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: expected 115, got {count}')
verify()