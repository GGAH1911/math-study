from sympy import *

def compute_sequence(a1):
    a = [None, a1]  # a[1] = a_1
    for n in range(1, 5):
        if a[n] > n:
            a_next = a[n]
        else:
            a_next = 3*n - 2 - a[n]
        a.append(a_next)
    return a[5]

candidates = [5, -4, 2, -1]
for a1 in candidates:
    a5 = compute_sequence(a1)
    print(f'a_1 = {a1}: a_5 = {a5}')
    if a5 != 5:
        print('VERIFY_FAIL')
        exit()

print('VERIFY_PASS')