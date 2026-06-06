a = [0] * 33
a[1], a[2] = 3, 4
a[3] = a[1] - 3
a[4] = a[2] + 3
a[5] = a[3] - 3
a[6] = a[4] + 3
for i in range(7, 33):
    a[i] = a[i - 6]
total = sum(a[1:33])
if total == 112:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')