from sympy import Rational, S

k = 9

def count_natural_solutions(k):
    count = 0
    found = []
    for n in range(1, 10000):
        fn = -(n - 2)**2 + k
        # A = sqrt(3^f(n)) = 3^(f(n)/2), always positive
        # product of real 4th roots of A = -A^(1/2) = -3^(f(n)/4)
        # condition: -3^(f(n)/4) = -9  <=>  f(n)/4 = 2  <=>  f(n) = 8
        # but verify using original formula numerically:
        import math
        A = 3 ** (fn / 2)  # float; always positive
        prod = -(A ** 0.5)  # product of real 4th roots
        # also verify f(n) == 8 directly
        if abs(fn - 8) < 1e-9:
            count += 1
            found.append(n)
        if n > 10000:
            break
    return count, found

count, found = count_natural_solutions(k)

# Also verify product condition directly for found n's
all_ok = True
for n in found:
    fn = -(n - 2)**2 + k
    import math
    A = 3 ** (fn / 2)
    prod = -(A ** 0.5)
    if abs(prod - (-9)) > 1e-9:
        all_ok = False

if count == 2 and all_ok:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: count={count}, found={found}, all_ok={all_ok}')
