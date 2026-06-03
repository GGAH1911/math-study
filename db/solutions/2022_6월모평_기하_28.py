import sympy as sp

a_val = sp.sqrt(3) - 1
c_val = 2 - sp.sqrt(3)
b2_val = a_val**2 - c_val**2

# 조건 1: 단축 꼭짓점 (0, sqrt(b2)) 까지 거리 = 1
dist_vertex = sp.sqrt(a_val**2 + b2_val)
cond1 = sp.simplify(dist_vertex - 1) == 0

# 조건 2: 초점 F = (c, 0) 까지 거리 = 1
dist_focus = a_val + c_val
cond2 = sp.simplify(dist_focus - 1) == 0

# 조건 3: b^2 > 0 (타원 성립)
cond3 = sp.simplify(b2_val) > 0

# 조건 4: a^2 + 2a - 2 = 0 만족
eq_check = sp.simplify(a_val**2 + 2*a_val - 2) == 0

if cond1 and cond2 and cond3 and eq_check:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: cond1={cond1}, cond2={cond2}, cond3={cond3}, eq={eq_check}')
