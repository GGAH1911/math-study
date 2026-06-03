import sympy as sp
x = sp.Symbol('x')
k_val = 10
f = x**3 - 3*x**2 - 9*x + k_val

# 극솟값이 -17인지 확인
f_at_3 = f.subs(x, 3)
assert f_at_3 == -17, f'극솟값 오류: {f_at_3}'

# 극댓값이 15인지 확인
f_at_minus1 = f.subs(x, -1)
assert f_at_minus1 == 15, f'극댓값 오류: {f_at_minus1}'

print('VERIFY_PASS')