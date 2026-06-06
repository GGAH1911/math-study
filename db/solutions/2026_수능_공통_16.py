a = [0, 1]
n = 1
a.append(n**2 * a[n] + 1)
n = 2
a.append(n**2 * a[n] + 1)
if a[3] == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')