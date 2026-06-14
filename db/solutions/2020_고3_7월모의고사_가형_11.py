import math

# 수열 계산
a = [0, 1]  # a[0]은 미사용, a[1] = 1

for n in range(1, 13):
    if a[n] <= 1:
        a_next = 2 ** a[n]
    else:
        a_next = math.log(math.sqrt(2)) / math.log(a[n])
    a.append(a_next)

a12 = a[12]
a13_computed = math.log(math.sqrt(2)) / math.log(a12) if a12 > 1 else 2 ** a12

product = a12 * a13_computed
sqrt2 = math.sqrt(2)

if abs(product - sqrt2) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')