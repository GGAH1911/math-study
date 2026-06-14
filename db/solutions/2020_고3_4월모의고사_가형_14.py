import cmath

def count_real_nth_roots(z, n):
    """Calculate number of real n-th roots of z"""
    if z == 0:
        return 1
    elif z > 0:
        if n % 2 == 1:
            return 1  # one positive real root
        else:
            return 2  # positive and negative roots
    else:  # z < 0
        if n % 2 == 1:
            return 1  # one negative real root
        else:
            return 0  # no real roots

total = 0
for n in range(2, 11):
    z = n - 5
    f_n = count_real_nth_roots(z, n)
    total += f_n

if total == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')