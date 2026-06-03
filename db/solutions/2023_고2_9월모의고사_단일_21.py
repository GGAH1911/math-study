a = [None]*22
b = [None]*7
b[6] = 18
for k in range(5, 0, -1):
    b[k] = 3*k - b[k+1]
for k in range(1, 7):
    a[3*k-2] = b[k]
    a[3*k-1] = ((-1)**k)*b[k]
    a[3*k]   = -b[k]
a[21] = -a[18]-18
a[20] = a[21]
a[19] = -a[20]
passed = True
for n in range(1, 21):
    if n % 3 != 0:
        if abs(a[n+1] - ((-1)**n)*a[n]) > 1e-9:
            passed = False
for n in [3,6,9,12,15,18]:
    if abs(a[n+3] - (-a[n]-n)) > 1e-9:
        passed = False
if abs(a[20]+a[21]) > 1e-9:
    passed = False
total = sum(a[k] for k in range(1,19))
if passed and abs(total-63)<1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')