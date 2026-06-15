import sympy as sp

CANDIDATE = 6

# 함수 정의
x = sp.Symbol('x')
y = (2*x - 7) / (x - 3)

# 수직 점근선: 분모 = 0
vertical_asymptotes = sp.solve(x - 3, x)
a = vertical_asymptotes[0]  # a = 3

# 수평 점근선: x → ∞일 때의 극한
horizontal_asymptote = sp.limit(y, x, sp.oo)
b = horizontal_asymptote  # b = 2

# 곱 계산
product = a * b

# 검증
if product == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')