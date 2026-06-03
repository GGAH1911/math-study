result = []
for x in range(-100, 101):
    if (x*x - x - 6 >= 0) and (x*x - 25 < 0):
        result.append(x)
total = sum(result)
expected = -2
print('VERIFY_PASS' if total == expected else 'VERIFY_FAIL')