from itertools import product
count = 0
valid_pairs = []
for m in range(1, 6):
    for n in range(1, 6):
        real = (m - n)
        imag = (m + n - 4)
        z_squared_real = real**2 - imag**2
        z_squared_imag = 2 * real * imag
        if z_squared_imag == 0:
            count += 1
            valid_pairs.append((m, n))
if count == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')