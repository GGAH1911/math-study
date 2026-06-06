from sympy import symbols, solve, simplify

a = symbols('a', positive=True, real=True)

# 넓이 조건: 그림1 넓이 = 그림2 넓이
area_fig1 = 2*a**3 - a
x = 2*a**2 - 1  # 그림2의 가로
area_fig2 = a * x

# 넓이가 같은지 확인
equation = area_fig1 - area_fig2
simplified = simplify(equation)

# a = 3/2일 때 검증
a_val = 3/2
fig1_area = 2*(a_val)**3 - a_val
fig2_width = 2*(a_val)**2 - 1
fig2_area = a_val * fig2_width
perimeter = 2 * (fig2_width + a_val)

if abs(fig1_area - fig2_area) < 1e-10 and abs(perimeter - 10) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')