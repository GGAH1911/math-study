import sympy as sp
k = sp.Symbol('k')
a1, a2 = 2, 4
b1, b2 = -1, k
# 벡터 평행 조건: 외적 = 0
condition = a1 * b2 - a2 * b1
solution = sp.solve(condition, k)
print(f'k = {solution[0]}')
if solution[0] == -2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')