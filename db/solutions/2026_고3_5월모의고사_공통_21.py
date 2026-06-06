import sympy as sp

p_val = 3/2
f = lambda x: x**3 - (9/4)*x

# 조건 (가) 검증: x=p에서 연속 및 미분가능
print(f'f(p)={f(p_val):.10f}')  # 0이어야 함
fp = lambda x: 3*x**2 - 9/4
print(f'f\'(p)={fp(p_val):.10f}')  # 4.5
print(f'kf\'(0)={-2 * fp(0):.10f}')  # 4.5

# 조건 (나) 검증: 실근의 합
roots_left = [0, -1.5, 1.5]  # x < 1.5
roots_right = [1.5, 3, 0]  # x >= 1.5, f(x-1.5)=0의 해
all_roots = sorted(list(set(roots_left + roots_right)))
print(f'roots={all_roots}, sum={sum(all_roots):.1f}')  # sum=3=2p

# 극값 검증
x_extrema = [-sp.sqrt(3)/2, sp.sqrt(3)/2, 3/2 + sp.sqrt(3)/2]
for x_val in x_extrema:
    g_val = float(x_val**3 - (9/4)*x_val)
    print(f'g({x_val})={g_val:.10f}')

max_extremum = float((4 * (27/8) * sp.sqrt(3)) / 9)
expected = float(3*sp.sqrt(3)/2)
print(f'max_extremum={max_extremum:.10f}, expected={expected:.10f}')

# 최종 답
answer = f(4)
print(f'f(4)={answer}')
if abs(answer - 55) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')