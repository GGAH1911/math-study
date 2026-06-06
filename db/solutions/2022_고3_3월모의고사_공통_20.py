# Verify a_1 = 7/4 produces a_7 = -1
a = [7/4]  # a_1

# Generate sequence up to a_7
for n in range(6):
    a_n = a[-1]
    if a_n < 0:
        a_next = -2 * a_n
    else:
        a_next = a_n - 2
    a.append(a_next)

# Check if a_7 = -1
if abs(a[6] - (-1)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')