def verify():
    def check_sequence(a1, a2, target=63):
        a = [a1, a2]
        for _ in range(3):
            if a[-1] * a[-2] % 2 == 1:
                a.append(a[-1] + a[-2])
            else:
                a.append(a[-1] + a[-2] - 2)
            if a[-1] <= 0:
                return False
        return a[4] == target
    
    solutions_a = [(29, 3), (23, 7), (17, 11), (11, 15), (5, 19)]
    solutions_c = [(30, 3), (24, 7), (18, 11), (12, 15), (6, 19)]
    
    for a1, a2 in solutions_a + solutions_c:
        if not check_sequence(a1, a2):
            print('VERIFY_FAIL')
            return
    
    a1_vals = [a1 for a1, a2 in solutions_a + solutions_c]
    if max(a1_vals) - min(a1_vals) == 25:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify()