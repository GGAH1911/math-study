import numpy as np

# n과 f(n) 정의
f_values = {}
for n in range(2, 21):
    a = 2**(n-3) - 8
    if a < 0:
        f_values[n] = 1 if n % 2 == 1 else 0
    elif a == 0:
        f_values[n] = 1
    else:  # a > 0
        f_values[n] = 1 if n % 2 == 1 else 2

# m=14일 때 합
m = 14
total = sum(f_values[n] for n in range(2, m+1))

if total == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Sum for m=14: {total}')