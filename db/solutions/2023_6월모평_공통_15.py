from sympy import symbols, Rational, simplify

k_values = [1, 3, 10]
results = []

for k in k_values:
    a = [0]  # a[0] represents a_1
    for n in range(1, 22):
        if a[-1] <= 0:
            a.append(a[-1] + Rational(1, k+1))
        else:
            a.append(a[-1] - Rational(1, k))
    results.append((k, a[21]))  # a[21] is a_22 (0-indexed)

verify_all = all(val == 0 for k, val in results)

if verify_all and len([k for k, v in results if v == 0]) == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')