# a1=1, a_{n+1}+3a_n=(-1)^n·n. a5?
CANDIDATE = 139
a = {1: 1}
for n in range(1, 5):
    a[n+1] = (-1)**n * n - 3*a[n]
print('VERIFY_PASS' if a[5] == CANDIDATE else 'VERIFY_FAIL')
