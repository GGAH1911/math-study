def f(x, a):
    return x**3 + a*x**2 - 7

a = 4
remainder = f(2, a)
if remainder == 17:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')