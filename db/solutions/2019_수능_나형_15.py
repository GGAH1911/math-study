
from sympy import log, Integer, symbols, solve, Rational

# Find all n >= 2 (natural numbers) such that 5*log_n(2) is a natural number
# Equivalent to: n^k = 32 for some natural number k, with n >= 2 integer

valid_n = []
for n in range(2, 1000):
    # Check if 5 * log(2)/log(n) is a natural number
    # i.e., log(2)/log(n) = k/5 for some natural k
    # i.e., n^k = 32 for some natural k
    # Check for k = 1 to 5 (since n >= 2, n^6 >= 64 > 32)
    for k in range(1, 40):
        val = n ** k
        if val == 32:
            valid_n.append(n)
            break
        elif val > 32:
            break

expected_sum = 34
computed_sum = sum(valid_n)

if computed_sum == expected_sum:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: valid_n={valid_n}, sum={computed_sum}, expected={expected_sum}')
