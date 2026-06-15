import sympy as sp
from sympy import symbols, solve, simplify

x, k = symbols('x k', real=True)

# 원래 방정식
eq = 4**x - k * 2**(x+1) + 16

# t = 2^x로 치환한 형태
t = symbols('t', positive=True, real=True)
eq_t = t**2 - 2*k*t + 16

# k=4일 때 확인
k_val = 4
eq_t_k4 = eq_t.subs(k, k_val)
roots_t = solve(eq_t_k4, t)
print(f'k=4일 때 t의 근: {roots_t}')

# t = 4일 때 x 값
t_val = 4
x_val = solve(2**x - t_val, x)
print(f't=4일 때 x의 값: {x_val}')
alpha = x_val[0]

# 원래 방정식에 대입하여 검증
verify = eq.subs([(k, k_val), (x, alpha)])
verify_simplified = simplify(verify)
print(f'x={alpha}를 원래 방정식에 대입: {verify_simplified}')

# 최종 답
ans = k_val + alpha
print(f'k + alpha = {k_val} + {alpha} = {ans}')

if verify_simplified == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')