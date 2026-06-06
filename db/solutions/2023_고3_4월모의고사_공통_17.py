import sympy as sp
from sympy import symbols, Rational, simplify

a = symbols('a', real=True)

# 점 (3/2, 5)를 평행이동된 함수 y = 4^(x-1) + a에 대입
x_val = Rational(3, 2)
y_val = 5

# 4^(3/2 - 1) + a = 5
# 4^(1/2) + a = 5
result = 4**(x_val - 1) + a - y_val
equation = sp.Eq(4**(x_val - 1) + a, y_val)
solution = sp.solve(equation, a)[0]

print(f'a = {solution}')

# 검증: 점 (3/2, 5)가 y = 4^(x-1) + 3 위에 있는지 확인
y_check = 4**(x_val - 1) + 3
if y_check == y_val:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')