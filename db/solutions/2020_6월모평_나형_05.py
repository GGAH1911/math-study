from sympy import symbols, Abs, solve

x, a = symbols('x a', real=True)

# 조건 p 풀이
eq_p = Abs(x - 4) - 2
sol_p = solve(eq_p, x)
print(f'p의 해: {sol_p}')

# p의 해는 x=2, x=6
p_solutions = [2, 6]

# p가 q의 충분조건: p⟹q
# p가 참인 모든 x에 대해 x≥a가 성립해야 함
# 따라서 min(p_solutions) ≥ a이어야 함
min_p = min(p_solutions)
print(f'p의 최솟값: {min_p}')
print(f'a의 최댓값: {min_p}')

# 검증: a=2일 때
a_max = 2
for x_val in p_solutions:
    if x_val >= a_max:
        print(f'x={x_val}: {x_val} >= {a_max} (참)')
    else:
        print(f'x={x_val}: {x_val} >= {a_max} (거짓)')

if all(x_val >= a_max for x_val in p_solutions):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')