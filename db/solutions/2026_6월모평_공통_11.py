import sympy as sp
t = sp.Symbol('t', real=True, positive=True)
x = t**3 - t**2 - t + 1
v = sp.diff(x, t)
a = sp.diff(v, t)

# 보기 나 검증: t=1일 때 속도
v_at_1 = v.subs(t, 1)
assert v_at_1 == 0, f'나 거짓: v(1)={v_at_1}'

# 보기 다 검증: 운동방향 변화 시각(t≥0)에서 가속도가 4
velocity_zeros = [sol for sol in sp.solve(v, t) if sol >= 0]
assert len(velocity_zeros) > 0, '운동방향 변화 시각이 없음'

for t_change in velocity_zeros:
    a_at_change = a.subs(t, t_change)
    if a_at_change == 4:
        print('VERIFY_PASS')
        break
else:
    print('VERIFY_FAIL')