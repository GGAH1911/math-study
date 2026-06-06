import sympy as sp

a_val, b_val, c_val = 8, 4, 10
x, y = sp.symbols('x y')

# 원래 원: x^2 + (y+4)^2 = 10
# 평행이동 적용: x축 -4, y축 +2
# 변환 후 표준형: (x+4)^2 + (y+2)^2 = 10

standard_form = (x + 4)**2 + (y + 2)**2 - 10
expanded = sp.expand(standard_form)

# x^2 + y^2 + ax + by + c = 0 형식
expected = x**2 + y**2 + a_val*x + b_val*y + c_val

if sp.expand(expanded) == sp.expand(expected):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')