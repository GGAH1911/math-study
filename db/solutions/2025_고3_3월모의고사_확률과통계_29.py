def count_satisfying():
    count = 0
    for a in range(1, 7):
        for b in range(1, 7):
            for c in range(1, 7):
                for d in range(1, 7):
                    product = a * b * c * d
                    if product % 16 == 0:
                        count += 1
    return count

result = count_satisfying()
if result == 363:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')