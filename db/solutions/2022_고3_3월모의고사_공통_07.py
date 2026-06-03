from sympy import symbols, diff, integrate

x = symbols('x')

# 원래 곡선
f = x**2 - 4*x + 6

# A(3,3)에서의 접선 (원래 문제 조건 그대로)
slope = diff(f, x).subs(x, 3)  # 2
tangent = slope * (x - 3) + 3  # 2x - 3

# 접점 확인: A(3,3)이 곡선 위에 있는지
assert f.subs(x, 3) == 3, 'A not on curve'
assert tangent.subs(x, 3) == 3, 'A not on tangent'

# y축(x=0)부터 접점(x=3)까지 둘러싸인 넓이
area = integrate(f - tangent, (x, 0, 3))

if area == 9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: area = {area}')
