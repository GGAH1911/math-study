from sympy import Matrix
a = Matrix([1, 0])
b = Matrix([1, 1])
result = a + 2*b
sum_of_components = sum(result)
if sum_of_components == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')