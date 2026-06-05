def verify_sequence(a1):
    a = [a1]
    for n in range(14):
        if a[-1] >= 0:
            a.append(a[-1] - 2)
        else:
            a.append(a[-1] + 5)
    return a[14]

result = verify_sequence(5)
if result < 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')