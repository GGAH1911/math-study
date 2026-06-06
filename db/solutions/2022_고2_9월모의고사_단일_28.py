import numpy as np
from sympy import symbols, solve

k = 3
n_even = [2, 4, 6, 8, 10, 12, 14, 16, 18]
sum_f = 0

for n in n_even:
    g_n = n**2 - 17*n + 19*k
    if g_n > 0:
        f_n = 2
    elif g_n == 0:
        f_n = 1
    else:
        f_n = 0
    sum_f += f_n

n_odd = [3, 5, 7, 9, 11, 13, 15, 17, 19]
sum_f += len(n_odd)

if sum_f == 19:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')