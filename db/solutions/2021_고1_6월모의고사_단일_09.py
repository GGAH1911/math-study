from sympy import I, simplify, expand

x = -2 + 3*I
y = 2 + 3*I

# 원래 식 계산
result = x**3 + x**2*y - x*y**2 - y**3
result_simplified = simplify(result)

# 답이 144인지 확인
if result_simplified == 144:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result_simplified}')