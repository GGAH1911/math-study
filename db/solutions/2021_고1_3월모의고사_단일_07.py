from statistics import median
data = [4, 5, 11, 12, 14, 17, 17, 20, 21, 21, 25, 28, 29, 34, 34, 38, 39, 40, 40, 42]
result = median(data)
if result == 23:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')