def a_n(n):
    if n % 2 == 1:  # n이 홀수
        return ((n + 1) ** 2) / 2
    else:  # n이 짝수
        return (n ** 2) / 2 + n + 1

total = sum(a_n(n) for n in range(1, 11))
result = 255

if abs(total - result) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')