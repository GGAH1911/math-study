k = 1
integers_sum = 0
valid_integers = []
for x in range(-10, 20):
    cond1 = abs(x - k) <= 5
    cond2 = x**2 - x - 12 > 0
    if cond1 and cond2:
        valid_integers.append(x)
        integers_sum += x
if integers_sum == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')