from sympy import symbols, Eq, solve
m1, m2, s = symbols('m1 m2 s', positive=True)
# 조건 도출: m1+m2=52, (24-m1)/s=2, (36-m2)/s=2
sol = solve([Eq(m1+m2,52), Eq(24-m1,2*s), Eq(36-m2,2*s)], [m1,m2,s])
m1_v = float(sol[m1])  # 20
s_v  = float(sol[s])   # 2
# 표준화
z_lo = (18 - m1_v) / s_v  # -1.0
z_hi = (21 - m1_v) / s_v  # 0.5
# 표준정규분포표 값
table = {0.5:0.1915, 1.0:0.3413, 1.5:0.4332, 2.0:0.4772}
result = table[abs(z_lo)] + table[z_hi]  # 0.3413+0.1915
# 조건 검증
assert abs(m1_v-20)<1e-9 and abs(s_v-2)<1e-9, 'params wrong'
assert abs(result-0.5328)<1e-6, f'got {result}'
print('VERIFY_PASS')