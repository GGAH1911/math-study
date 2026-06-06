f = lambda x: x + 3
g = lambda x: x**2 + 1
result = g(f(9))
expected = 145
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')