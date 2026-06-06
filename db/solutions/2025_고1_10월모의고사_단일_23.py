from math import comb, perm
n = 13
left = comb(n, 2)
right = perm(3, 2) * n
if left == right:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')