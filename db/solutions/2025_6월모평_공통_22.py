from fractions import Fraction

def verify_a1(a1):
    a = {1: a1, 2: -a1}
    for n in range(2, 15):
        sqrt_n_int = int(n**0.5)
        if sqrt_n_int * sqrt_n_int == n and a[n] > 0:
            a[n+1] = a[n] - sqrt_n_int * a[sqrt_n_int]
        else:
            a[n+1] = a[n] + 1
    return a[15]

values = [Fraction(-7, 4), -11, 12]
results = [verify_a1(v) for v in values]

if all(r == 1 for r in results):
    product = 1
    for v in values:
        product *= v
    if product == 231:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')