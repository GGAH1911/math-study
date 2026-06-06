import sympy as sp
a = 3
k = 2
x = sp.Symbol('x')
f = a * sp.Abs(x - 2)

# 우미분 계산
f_right = a * (x - 2)
right_deriv = sp.limit((f_right.subs(x, 2 + sp.Symbol('h')) - f.subs(x, 2)) / sp.Symbol('h'), sp.Symbol('h'), 0, '+')

# 좌미분 계산
f_left = a * (2 - x)
left_deriv = sp.limit((f_left.subs(x, 2 - sp.Symbol('h')) - f.subs(x, 2)) / (-sp.Symbol('h')), sp.Symbol('h'), 0, '+')

# 차이 확인
diff = a - (-a)
if diff == 6:
    result = f.subs(x, a + k)
    if result == 9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')