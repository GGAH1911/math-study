# 점화식: a_{n+1} = n*a_n + 2, a_1 = 1
# 답: a_3 = 8
a = [0, 1]  # a[0]은 미사용, a[1] = a_1
n = 1
while len(a) <= 3:
    a_next = n * a[n] + 2
    a.append(a_next)
    n += 1
a_3 = a[3]
if a_3 == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')