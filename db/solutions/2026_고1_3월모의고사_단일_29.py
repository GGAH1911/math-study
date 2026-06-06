def f(x, a):
    return a*x**2 - 3*a*x - 4*a**2 - 8*a - 2

answer = 6
f1_sum = sum(f(1, a) for a in [-2, -1])

for a in [-2, -1]:
    B_y = f(0, a)
    A_x = 1.5
    area = 0.5 * abs(A_x) * abs(B_y)
    if abs(area - 1.5) > 1e-9:
        print('VERIFY_FAIL')
        exit()

if f1_sum == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')