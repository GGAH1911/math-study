from fractions import Fraction
from sympy import isprime

cards_A = [1, 1, 2, 2, 3, 3]
cards_B = [3, 3, 4, 4, 5, 5]

total_A, prime_A = 0, 0
for i in range(len(cards_A)):
    for j in range(i+1, len(cards_A)):
        total_A += 1
        if isprime(cards_A[i] + cards_A[j]):
            prime_A += 1

total_B, prime_B = 0, 0
for i in range(len(cards_B)):
    for j in range(i+1, len(cards_B)):
        total_B += 1
        if isprime(cards_B[i] + cards_B[j]):
            prime_B += 1

p_all_heads = Fraction(1, 8)
p_not_all = Fraction(7, 8)
p_total = p_all_heads * Fraction(prime_A, total_A) + p_not_all * Fraction(prime_B, total_B)

print('VERIFY_PASS' if p_total == Fraction(37, 120) else f'VERIFY_FAIL: got {p_total}')