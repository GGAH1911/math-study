from itertools import combinations

numbers = list(range(1, 9))
all_combos = list(combinations(numbers, 3))

even_sum = [(a,b,c) for a,b,c in all_combos if (a+b+c) % 2 == 0]
a_odd = [combo for combo in even_sum if combo[0] % 2 == 1]

prob = len(a_odd) / len(even_sum)
expected = 5 / 7

if abs(prob - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')