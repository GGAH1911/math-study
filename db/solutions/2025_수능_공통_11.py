from sympy import symbols, diff, solve, simplify
import numpy as np

t = symbols('t')
x = t**3 - 3*t**2/2 - 6*t
v = diff(x, t)
a = diff(v, t)

# 운동 방향이 바뀌는 시각 (v=0, t>=0)
t_values = solve(v, t)
t_change = [val for val in t_values if val >= 0]
print(f'Direction change at t={t_change}')

if t_change:
    t_val = t_change[0]
    a_val = a.subs(t, t_val)
    print(f'Acceleration at t={t_val}: {a_val}')
    
    # 검증: t=2에서 속도가 0인지 확인
    v_at_2 = v.subs(t, 2)
    print(f'Velocity at t=2: {v_at_2}')
    
    if v_at_2 == 0 and a_val == 9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')