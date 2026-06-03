import sympy as sp

a = sp.Rational(-1, 2)
b = sp.Rational(4, 1)

# 이동 후 함수: y = 4^(x - a) - 6 + b
x = sp.Symbol('x')
f = 4**(x - a) - 6 + b

# 조건 1: 원점 통과
val_at_origin = f.subs(x, 0)
assert val_at_origin == 0, f'원점 통과 실패: f(0) = {val_at_origin}'

# 조건 2: 점근선이 y = -2 (x -> -inf일 때 극한)
limit_val = sp.limit(f, x, -sp.oo)
assert limit_val == -2, f'점근선 실패: limit = {limit_val}'

# ab 값 확인
ab = a * b
assert ab == -2, f'ab 실패: {ab}'

print('VERIFY_PASS')
