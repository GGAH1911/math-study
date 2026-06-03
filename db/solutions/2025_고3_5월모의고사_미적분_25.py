import sympy as sp

# 변수 정의
n = sp.Symbol('n', positive=True, integer=True)
a = 4
b = 2

# 좌변 계산
left_side = sp.sqrt(a*n**2 + b*n) - b*n
left_limit = sp.limit(left_side, n, sp.oo)

# 우변 계산
right_side = (b*n - 1)**2 / ((b+6)*n**2 + 1)
right_limit = sp.limit(right_side, n, sp.oo)

# 검증
if sp.simplify(left_limit - right_limit) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')