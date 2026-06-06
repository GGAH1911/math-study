import sympy as sp
a1_values = [sp.Rational(1,3), sp.Rational(2,3), sp.Rational(5,3), 2]
total = 0
for a1 in a1_values:
    a = [0, a1]
    for n in range(1, 15):
        if n > 1:
            if n % 2 == 0:
                a.append(1 - a[n-1])
            else:
                a.append(1 / a[n-1])
    s = sum(abs(a[i]) - a[i] for i in range(1, 15))
    if s != 10:
        print('VERIFY_FAIL')
        exit()
    total += a1
if abs(total - sp.Rational(14,3)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')