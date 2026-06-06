import sympy as sp
x, k = sp.symbols('x k', real=True)

# 조건 q: x^2 - 8x + 12 = 0의 해
q_solutions = sp.solve(x**2 - 8*x + 12, x)
print(f'q 조건의 해: {q_solutions}')  # [2, 6]

# 답 k = 11로 검증
k_val = 11
for x_val in q_solutions:
    p_satisfied = (x_val + 5 <= k_val)
    print(f'x = {x_val}일 때: {x_val} + 5 = {x_val + 5} <= {k_val}? {p_satisfied}')

# 모든 q의 해가 p를 만족하는가?
all_satisfy = all(x_val + 5 <= k_val for x_val in q_solutions)
if all_satisfy:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')