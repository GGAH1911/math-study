from itertools import product
count = 0
valid_pairs = []
for a, b in product(range(1, 7), repeat=2):
    product_val = a * b
    is_divisor_of_4 = (4 % product_val == 0) if product_val > 0 else False
    is_multiple_of_12 = (product_val % 12 == 0)
    if is_divisor_of_4 or is_multiple_of_12:
        count += 1
        valid_pairs.append((a, b, product_val))
if count == 13:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')