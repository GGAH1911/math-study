from sympy import Matrix
A = Matrix([[-1, -2], [2, 3]])
A2 = A ** 2
A3 = A ** 3
A2_plus_A3 = A2 + A3
result_sum = sum(A2_plus_A3)
if result_sum == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')