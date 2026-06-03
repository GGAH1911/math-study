from fractions import Fraction

a1 = Fraction(-5, 2)
r = Fraction(-1, 2)

def a(n):
    return a1 * r**(n-1)

def b(n):
    an = a(n)
    abs_an = abs(an)
    if n % 2 == 0:
        return an          # even: a_n > 0 (forced)
    elif n == 1:
        return abs_an      # b_1 = |a_1|
    elif n == 3:
        return an          # b_3 = a_3 (min k=2 requires this)
    else:
        return abs_an      # odd n>=5: b_n = |a_n|

# Verify condition (가)
all_ga = all((b(n) - a(n)) * (b(n) - abs(a(n))) == 0 for n in range(1, 30))

# Verify condition (나): k=2 sum is 0
k2_ok = all(a(2*n+1) + b(2*n+1) == 0 for n in range(2, 200))

# Verify condition (나): k=1 sum is NOT 0
k1_fails = (a(3) + b(3) != 0)

# Verify b_1 - b_3 = 3a_3 + 5
cond_b = (b(1) - b(3) == 3*a(3) + 5)

# Compute infinite sum (exact)
even_sum = Fraction(5, 4) / (1 - Fraction(1, 4))          # 5/3
odd_first_two = b(1) + b(3)                                # 5/2 - 5/8 = 15/8
odd_tail = Fraction(5, 2) * Fraction(1, 16) / Fraction(3, 4)  # 5/24
total = even_sum + odd_first_two + odd_tail

if all_ga and k2_ok and k1_fails and cond_b and total == Fraction(15, 4):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: ga={all_ga}, k2={k2_ok}, k1_fail={k1_fails}, cond_b={cond_b}, total={total}')