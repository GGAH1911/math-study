def verify_conditions(a, b, c):
    digits = [a, b, c]
    count_7 = digits.count(7)
    product_mod2 = (a * c) % 2
    return count_7 == 1 and product_mod2 == 1

total = 0
for a in range(1, 10):
    for b in range(0, 10):
        for c in range(0, 10):
            if verify_conditions(a, b, c):
                total += 1

if total == 88:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')