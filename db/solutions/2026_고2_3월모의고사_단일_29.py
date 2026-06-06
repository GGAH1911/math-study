import numpy as np
from sympy import symbols, solve, sqrt, simplify

# a12 + a21 = 3, a12*a21 = -2를 만족하는 a12, a21 구하기
t = symbols('t')
eq = t**2 - 3*t - 2
roots = solve(eq, t)
a12_val = roots[0]  # (3 + sqrt(17))/2
a21_val = roots[1]  # (3 - sqrt(17))/2

# 행렬 A와 B 구성
A = np.array([[0, float(a12_val), ], [float(a21_val), 0]])
A = np.array([[0, float(a12_val)], [float(a21_val), 0]])
B = A @ A

# A^2 = B 확인
A_sq_check = np.allclose(A @ A, B)

# 조건 (가) 확인: a_ij * b_ij = 0
product_check = np.allclose(A * B, 0)

# 조건 (나) 확인: a_ij + b_ij != 0
sum_nonzero = np.all(A + B != 0)

# A+B 확인
AplusB = A + B
sum_all = np.sum(AplusB)
prod_all = np.prod(AplusB)

# a12^3 + a21^3 계산
result = a12_val**3 + a21_val**3
result_simplified = simplify(result)

if A_sq_check and product_check and sum_nonzero and np.isclose(sum_all, -1) and np.isclose(prod_all, -8) and result_simplified == 45:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')