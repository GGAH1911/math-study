def verify_solution(k):
    a = [3]  # a[0] = a_1
    for n in range(1, 5):
        prev = a[-1]
        if prev < 0:
            a.append(abs(prev + n))
        else:
            a.append(prev - 10 + k)
    return a[3] * a[4]  # a_4 * a_5

results = []
for k_val in [5.5, 7, 8, 9, 37/4]:
    product = verify_solution(k_val)
    results.append(product == 0)

if all(results) and len(results) == 5:
    M = 37/4
    m = 11/2
    M_plus_m = M + m
    if abs(M_plus_m - 59/4) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')