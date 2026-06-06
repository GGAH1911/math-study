import sympy as sp
from sympy import sqrt, symbols, solve, simplify

# 변수 설정
h, a = symbols('h a', positive=True, real=True)

# 조건: a = h/sqrt(2)
a_expr = h / sqrt(2)

# 외심의 y 좌표
y_O = (h**2 - a_expr**2) / (2*h)
y_O = simplify(y_O)
print(f'y_O = {y_O}')  # h/4

# AO와 OE
AO = h - y_O
OE = y_O
print(f'AO = {simplify(AO)}')
print(f'OE = {simplify(OE)}')
print(f'AO/OE = {simplify(AO/OE)}')  # 3

# 삼각형 ADO의 넓이 = 3ah/16
area_ADO = 3 * a_expr * h / 16
print(f'Area ADO = {simplify(area_ADO)}')  # 3h^2/(16*sqrt(2))

# 조건: 넓이 = 6
eq = area_ADO - 6
h_val = solve(eq, h)[0]
print(f'h = {h_val}')

a_val = h_val / sqrt(2)
print(f'a = {a_val}')

# ah 계산
product = simplify(a_val * h_val)
print(f'ah = {product}')

# 삼각형 ABC의 넓이 = ah
area_ABC = product
print(f'Area ABC = {area_ABC}')

# 검증
if area_ABC == 32:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')