k = 2
a = (k + 3, 3*k - 1)
b = (1, 1)

# 평행 조건 검사: 교차곱이 0
cross_product = a[0]*b[1] - a[1]*b[0]

if cross_product == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')