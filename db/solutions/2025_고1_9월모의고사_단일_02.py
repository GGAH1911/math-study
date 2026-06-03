import sympy as sp
a, b = 3, 9
# 행렬 A의 (1,2) 원소
assert a + 1 == 4, f'A의 (1,2) 원소: {a+1} != 4'
# 행렬 B의 (2,1) 원소
assert b - 1 == 8, f'B의 (2,1) 원소: {b-1} != 8'
# 최종 답
result = a * b
assert result == 27, f'a*b = {result} != 27'
print('VERIFY_PASS')