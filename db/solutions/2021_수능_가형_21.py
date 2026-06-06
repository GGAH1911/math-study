from sympy import Rational, sqrt

a1 = Rational(3, 4)
a2 = 1 / (1 - a1)

# Build terms step by step using the recurrences
a = {1: a1, 2: a2}

def get(n):
    if n in a:
        return a[n]
    # Use (가) or (나)
    if n % 2 == 0:  # n = 2k -> a2*a_k + 1
        k = n // 2
        val = a2 * get(k) + 1
    else:           # n = 2k+1 -> a2*a_k - 2
        k = (n - 1) // 2
        val = a2 * get(k) - 2
    a[n] = val
    return val

a8 = get(8)
a15 = get(15)

diff = a8 - a15
ratio = a8 / a1

if diff == 63 and ratio == 92:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: diff={diff}, ratio={ratio}')
