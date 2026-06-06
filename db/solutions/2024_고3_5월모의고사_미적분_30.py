from fractions import Fraction

# Solution: a = 5, r = -1/4, p = 4
a = 5
r = Fraction(-1, 4)
p = 4
alpha = Fraction(3, 64)  # value between |a_4| and |a_5|

def a_n(n):
    return a * (r ** (n - 1))

def b_n(n):
    val = a_n(n)
    if abs(val) < alpha:
        return val
    else:
        return Fraction(-5) / val

# Verify condition (가): sum of infinite geometric series
sum_inf = a / (1 - r)
assert sum_inf == 4, f'Sum should be 4, got {sum_inf}'

# Verify condition (나): sum up to p
sum_b_up_to_p = sum(b_n(n) for n in range(1, p + 1))
assert sum_b_up_to_p == 51, f'Sum b_n up to p should be 51, got {sum_b_up_to_p}'

# Verify sum from p+1 to infinity
sum_a_tail = (a * (r ** p)) / (1 - r)
assert sum_a_tail == Fraction(1, 64), f'Sum a_n from p+1 should be 1/64, got {sum_a_tail}'

# Verify minimum of sum(a_n/b_n) at m=p
cum_sums = []
for m in range(1, p + 3):
    s = sum(a_n(n) / b_n(n) for n in range(1, m + 1))
    cum_sums.append(float(s))

min_idx = cum_sums.index(min(cum_sums)) + 1
assert min_idx == p, f'Minimum should be at m={p}, got m={min_idx}'

# Final answer
a_3 = a_n(3)
answer = 32 * (a_3 + p)
assert answer == 138, f'Expected 138, got {answer}'

print('VERIFY_PASS')