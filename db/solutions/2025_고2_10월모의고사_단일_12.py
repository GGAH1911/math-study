import sympy as sp

t = sp.Symbol('t', positive=True)

# P의 x, y 좌표 (원래 문제의 두 식으로부터)
px = 3 + t
py = t * (3 + t)  # = px^2 - 3*px 와 같은지 확인

# 원래 곡선 y = x^2 - 3x에 P 대입
curve_y = px**2 - 3*px
line_y = t * px

assert sp.simplify(curve_y - py) == 0, 'P가 곡선 위에 없음'
assert sp.simplify(line_y - py) == 0, 'P가 직선 위에 없음'

# OH, OP 계산
OH = px  # t>0이므로 양수
OP = sp.sqrt(px**2 + py**2)

numerator = sp.simplify(OP - OH)
expr = sp.simplify(numerator / t**2)

lim_val = sp.limit(expr, t, 0, '+')

if lim_val == sp.Rational(3, 2):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {lim_val}')
