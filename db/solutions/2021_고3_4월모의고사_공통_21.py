def verify_a15(a1):
    a = a1
    for i in range(14):  # a1부터 a15까지 14번의 전이
        if a >= 0:
            a = a - 2
        else:
            a = a + 5
    return a

result = verify_a15(5)
if result < 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')