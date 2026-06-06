import sympy as sp

k = 4
a = -7
d = 2

S_k = k * (a + k - 1)
S_k_plus_2 = (k + 2) * (a + k + 1)

a_2k = a + (2 * k - 1) * d

if S_k == -16 and S_k_plus_2 == -12 and a_2k == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')