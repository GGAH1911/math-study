import sympy as sp
x, m = sp.symbols('x m')
f_prime = -x**2 + 4*x + m

# x=3에서 극값 조건: f'(3) = 0
eq = f_prime.subs(x, 3)
m_val = sp.solve(eq, m)[0]
print(f'm = {m_val}')

# 극대 검증: 2차 도함수
f_double_prime = sp.diff(f_prime, x)
f_double_prime_at_3 = f_double_prime.subs(x, 3).subs(m, m_val)
print(f'f\"(3) = {f_double_prime_at_3}')

# f"(3) < 0 ⟹ 극대
if f_double_prime_at_3 < 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')