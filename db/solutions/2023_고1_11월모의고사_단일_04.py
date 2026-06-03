total = sum(x for x in range(-1000, 1001) if 3*x >= 2*x + 3 and x - 10 <= -x)
print('VERIFY_PASS' if total == 12 else 'VERIFY_FAIL')