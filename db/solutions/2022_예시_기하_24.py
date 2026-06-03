import sympy as sp
x, y = sp.symbols('x y', real=True)
# 원래 조건: |OP|^2 - OA·OP = 3 → x^2+y^2 - 4x - 6y = 3
# 반지름 r=4, 중심 (2,3)이면 (x-2)^2+(y-3)^2=16 위의 점들이 조건 만족하는지 확인
# 매개변수 t로 원 위 임의점
t = sp.Symbol('t', real=True)
px = 2 + 4*sp.cos(t)
py = 3 + 4*sp.sin(t)
lhs = px**2 + py**2 - 4*px - 6*py
result = sp.simplify(lhs - 3)
if result == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', result)
