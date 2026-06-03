from sympy import symbols, simplify
m = symbols('m')
# 평행이동된 함수: y = 2^(-1) + m이 2가 되어야 함
result = 2**(-1) + 3/2
assert result == 2, f'Failed: {result} != 2'
print('VERIFY_PASS')