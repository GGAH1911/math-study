a = [0] * 23
a[1] = 1
for n in range(1, 22):
    if a[n] >= 0:
        a[n+1] = a[n] - 4
    else:
        a[n+1] = a[n] ** 2
total = sum(a[1:23])
print('VERIFY_PASS' if total == 58 else f'VERIFY_FAIL: got {total}')