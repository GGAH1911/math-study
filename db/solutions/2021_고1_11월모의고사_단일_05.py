import sympy as sp

x, y, a = sp.symbols('x y a')

# 원래 직선: 3x - 2y + a = 0
# 점 (x, y)가 원래 직선 위에 있음

# 원점 대칭: (x, y) -> (-x, -y)
# 대칭이동된 직선: 3(-x) - 2(-y) + a = 0 -> 3x - 2y - a = 0

# a = 5일 때 대칭이동된 직선: 3x - 2y - 5 = 0
# 점 (3, 2)를 지나는지 확인
a_val = 5
result = 3*3 - 2*2 - a_val

if abs(result) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')