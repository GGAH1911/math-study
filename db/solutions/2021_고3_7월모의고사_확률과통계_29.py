from math import gcd
def count_divisors(n):
    count = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            count += 1 + (1 if i != n // i else 0)
    return count

cards = []
for num in range(1, 6):
    cards.extend([num] * num)

condition_A = 0
condition_A_and_B = 0

for i in range(len(cards)):
    for j in range(i+1, len(cards)):
        product = cards[i] * cards[j]
        if count_divisors(product) <= 3:
            condition_A += 1
            if (cards[i] + cards[j]) % 2 == 0:
                condition_A_and_B += 1

g = gcd(condition_A_and_B, condition_A)
q, p = condition_A_and_B // g, condition_A // g
assert p + q == 25, f'Expected 25, got {p + q}'
print('VERIFY_PASS')