import numpy as np
from scipy.optimize import fsolve

# 점들의 좌표
A = np.array([-4, 1])
B = np.array([4, 1])
D = np.array([0, -3])

# 이차함수: f(x) = (1/4)x^2 - 3
def f(x):
    return 0.25 * x**2 - 3

# 조건 검증
# 1. A, B, D가 그래프 위의 점인지 확인
assert abs(f(A[0]) - A[1]) < 1e-9, f'f({A[0]}) should be {A[1]}'
assert abs(f(B[0]) - B[1]) < 1e-9, f'f({B[0]}) should be {B[1]}'
assert abs(f(D[0]) - D[1]) < 1e-9, f'f({D[0]}) should be {D[1]}'

# 2. 삼각형 ADB의 각도 확인 (직각)
vec_DA = A - D
vec_DB = B - D
dot_product = np.dot(vec_DA, vec_DB)
assert abs(dot_product) < 1e-9, f'angle ADB should be 90 degrees, dot product = {dot_product}'

# 3. DA = DB (이등변)
DA = np.linalg.norm(vec_DA)
DB = np.linalg.norm(vec_DB)
assert abs(DA - DB) < 1e-9, f'DA={DA} should equal DB={DB}'

# 4. 삼각형 넓이 = 16
area = 0.5 * DA * DB
assert abs(area - 16) < 1e-9, f'Area should be 16, got {area}'

# 5. 조건 (나): AC = 3*BC
C = np.array([2, 1])
AC = np.linalg.norm(A - C)
BC = np.linalg.norm(B - C)
assert abs(AC - 3*BC) < 1e-9, f'AC={AC} should equal 3*BC={3*BC}'

# 6. 이차항 계수 > 0 (확인됨: 0.25 > 0)

# f(8) 계산
result = f(8)
print('VERIFY_PASS')