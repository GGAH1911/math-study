count = 0
sols = []
for x in range(-100, 200):
    if (x + 6 <= 4*x) and (3*x + 4 < x + 16):
        count += 1
        sols.append(x)
print('VERIFY_PASS' if count == 4 and sols == [2,3,4,5] else 'VERIFY_FAIL')