def f(n):
    product = (2*n - 5) * (2*n - 9)
    if product == 0:
        return 1
    elif product > 0:
        return 1 if n % 2 == 1 else 2
    else:  # product < 0
        return 1 if n % 2 == 1 else 0

total = sum(f(n) for n in range(2, 9))
if total == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')