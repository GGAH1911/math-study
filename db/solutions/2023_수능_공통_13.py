from math import gcd
from functools import reduce

def prime_factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def count_divisors(n):
    if n == 1:
        return 1
    factors = prime_factorize(n)
    count = 1
    for exp in factors.values():
        count *= (exp + 1)
    return count

total = 0
for m in range(2, 10):
    factors = prime_factorize(m)
    if factors:
        d = reduce(gcd, factors.values())
    else:
        d = 1
    
    divisor_count = count_divisors(12 * d)
    f_m = divisor_count - 1
    total += f_m

if total == 47:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')