import sympy as sp

CANDIDATE = 12

t = sp.Symbol('t')
a_val = 0
b_val = -3

# 위치 함수
x = t**3 + a_val*t**2 + b_val*t

# 속도 (1차 미분)
v = sp.diff(x, t)
print(f'v(t) = {v}')
print(f'v(1) = {v.subs(t, 1)}')

# 가속도 (2차 미분)
acc = sp.diff(v, t)
print(f'a(t) = {acc}')
print(f'a(2) = {acc.subs(t, 2)}')

# 검증
v_at_1 = v.subs(t, 1)
acc_at_2 = acc.subs(t, 2)

if v_at_1 == 0 and acc_at_2 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')