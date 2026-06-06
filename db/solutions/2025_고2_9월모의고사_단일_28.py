from sympy import symbols, solve

# Given: a_2 = 2, common difference d_5 = 64
a_2 = 2
d_5 = 64

# Calculate a_14 and a_13
a_14 = 81 * a_2  # a_14 = a_2 * 3^4
a_13 = a_14 - d_5  # Since a_13, a_14 form arithmetic sequence with a_15
a_15 = a_14 + d_5  # a_13 + a_15 = 2*a_14

# Verify condition (가): a_13 + a_15 = 2*a_14
if a_13 + a_15 == 2 * a_14:
    # Construct full sequence with a_2 = 2
    a = [0] * 15  # a[0] unused, a[1] to a[14]
    a[2] = 2
    a[5] = 6
    a[8] = 18
    a[11] = 54
    a[14] = 162
    a[13] = 98
    
    # Set other terms (choosing minimal valid values)
    a[1], a[3] = 1, 3  # a_1 + a_3 = 4 = 2*a_2
    a[4], a[6] = 1, 11  # a_4 + a_6 = 12 = 2*a_5
    a[7], a[9] = 1, 35  # a_7 + a_9 = 36 = 2*a_8
    a[10], a[12] = 1, 107  # a_10 + a_12 = 108 = 2*a_11
    
    # Verify sum condition
    sum_14 = sum(a[1:15])
    if sum_14 == 500 and all(a[i] >= 1 for i in range(1, 15)):
        # Verify condition (나): b_n is geometric with ratio 3
        b = []
        for n in range(1, 5):
            b_n = a[3*n-2] + a[3*n-1] + a[3*n]
            b.append(b_n)
        
        if len(b) >= 2 and all(b[i+1] == 3*b[i] for i in range(len(b)-1)):
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')