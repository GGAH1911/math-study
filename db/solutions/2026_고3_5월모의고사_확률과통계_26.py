from itertools import product

# (a1, a5) 경우의 수
cases = [(1, 5), (2, 6)]
total = 0

for a1, a5 in cases:
    valid_values = list(range(a1, a5 + 1))
    for a2, a3, a4 in product(valid_values, repeat=3):
        product_val = a1 * a2 * a3 * a4 * a5
        if product_val % 2 == 0:  # 조건 (나): 짝수
            total += 1

if total == 223:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')