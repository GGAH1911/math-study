from sympy import symbols, solve, diff, simplify

# 원래 함수와 조건
x, a = symbols('x a', real=True)
f = x**3 - 3*a*x**2 + 3*(a**2 - 1)*x

# 극값 구하기
f_prime = diff(f, x)
extreme_points = solve(f_prime, x)
print(f'극값점: {extreme_points}')

# 극댓값 조건: f(a-1) = 4
a_val = a - 1
f_at_extreme = f.subs(x, a_val).simplify()
print(f'f(a-1) = {f_at_extreme}')

# 극댓값이 4
condition1 = f_at_extreme - 4
solutions_a = solve(condition1, a)
print(f'극댓값=4 조건: a = {solutions_a}')

# f(-2) > 0 확인
for sol in solutions_a:
    f_at_minus2 = f.subs([(x, -2), (a, sol)])
    print(f'a = {sol}: f(-2) = {f_at_minus2}')
    if f_at_minus2 > 0:
        valid_a = sol
        print(f'  → 조건 만족')
        
# 최종 답
f_final = f.subs(a, valid_a)
result = f_final.subs(x, -1)
print(f'\na = {valid_a}일 때 f(x) = {f_final}')
print(f'f(-1) = {result}')

# 검증
if result == 2:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')