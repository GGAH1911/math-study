from itertools import product

X = {1, 2, 3, 4, 5}
Y = {1, 2, 3}

count = 0
for f_vals in product(Y, repeat=5):
    f = {x: f_vals[x-1] for x in X}
    valid = True
    for x in X:
        if x * f[x] > 10:
            valid = False
            break
    if valid:
        count += 1

if count == 108:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')