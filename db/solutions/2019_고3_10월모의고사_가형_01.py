from sympy import symbols, Matrix

# 벡터 정의
a = Matrix([1, 2])
b = Matrix([-2, 5])

# 2a - b 계산
result = 2*a - b

# 성분의 합
sum_components = sum(result)

CANDIDATE = 3
if sum_components == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')