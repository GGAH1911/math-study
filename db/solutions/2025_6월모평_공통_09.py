import sympy as sp

a = sp.Rational(-5, 4)

# 원래 함수 정의
def f_left(x):
    return x - sp.Rational(1, 2)  # x < 0

def f_right(x):
    return -x**2 + 3  # x >= 0

# x=0에서의 좌극한: lim_{x->0^-} (f(x)+a)^2
left_lim = (f_left(sp.Integer(0)) + a)**2

# x=0에서의 값(우극한): (f(0)+a)^2
right_val = (f_right(sp.Integer(0)) + a)**2

# 연속 조건 확인
if sp.simplify(left_lim - right_val) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Left: {left_lim}, Right: {right_val}')
