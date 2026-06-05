import numpy as np

def compute_sequence(n_max):
    a = [0, 10]  # a[0] unused, a[1] = 10
    for n in range(1, n_max):
        if a[n] == int(a[n]):  # a_n is integer
            a_next = 5 - 10 / a[n]
        else:  # a_n is not integer
            a_next = -2 * a[n] + 3
        a.append(a_next)
    return a

a = compute_sequence(13)
a_9 = a[9]
a_12 = a[12]
result = a_9 + a_12

if abs(result - 8) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')