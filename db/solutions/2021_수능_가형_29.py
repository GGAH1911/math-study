def verify():
    count = 0
    for b_A in range(4, 7):
        for w_A in range(0, 7):
            if b_A + w_A < 1:
                continue
            if not (b_A > w_A):
                continue
            remaining_black = 6 - b_A
            remaining_white = 6 - w_A
            for b_B in range(0, remaining_black + 1):
                for b_C in range(0, remaining_black - b_B + 1):
                    b_D = remaining_black - b_B - b_C
                    for w_B in range(0, remaining_white + 1):
                        for w_C in range(0, remaining_white - w_B + 1):
                            w_D = remaining_white - w_B - w_C
                            if (b_B + w_B < 1 or b_C + w_C < 1 or 
                                b_D + w_D < 1):
                                continue
                            greater_count = sum([b_A > w_A, b_B > w_B, 
                                              b_C > w_C, b_D > w_D])
                            if greater_count == 2:
                                count += 1
    expected = 201
    if count == expected:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
verify()