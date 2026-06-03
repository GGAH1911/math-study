from fractions import Fraction

def x_n(n):
    exp = 6 - 2 * n
    if exp >= 0:
        return Fraction(2**exp)
    else:
        return Fraction(1, 2**(-exp))

# Verify the recurrence: x_{n+1} = x_n / 4
for n in range(1, 8):
    assert x_n(n + 1) == x_n(n) / 4, f'Recurrence failed at n={n}'

# Verify specific values
assert x_n(1) == Fraction(16)
assert x_n(5) == Fraction(1, 16)
assert x_n(6) == Fraction(1, 64)

# Count k where minimum n satisfying x_n < 1/k is exactly 6
count = 0
for k in range(1, 500):
    one_over_k = Fraction(1, k)
    min_n = None
    for n in range(1, 50):
        if x_n(n) < one_over_k:
            min_n = n
            break
    if min_n == 6:
        count += 1

if count == 48:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: count={count}')
