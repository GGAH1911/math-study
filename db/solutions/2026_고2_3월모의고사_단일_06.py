# 이차정방행렬 A, a_ij = i + j (i=1,2, j=1,2)
matrix_sum = 0
for i in range(1, 3):
    for j in range(1, 3):
        a_ij = i + j
        matrix_sum += a_ij

if matrix_sum == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')