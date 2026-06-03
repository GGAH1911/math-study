ints = [x for x in range(-100, 101) if (x*x - x - 12 <= 0) and (x*x - 3*x + 2 > 0)]
total = sum(ints)
print('VERIFY_PASS' if total == 1 else 'VERIFY_FAIL')