import sympy as sp
x = sp.Symbol('x')
f = 2*x**3 + 3*x**2 - 12*x - 8
k_candidate = 15

# 구간 [-2, 2]에서 함수값 평가
f_at_neg2 = f.subs(x, -2)
f_at_1 = f.subs(x, 1)
f_at_2 = f.subs(x, 2)

max_abs = max(abs(f_at_neg2), abs(f_at_1), abs(f_at_2))

if max_abs == k_candidate:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: max|f(x)| = {max_abs}, k = {k_candidate}')