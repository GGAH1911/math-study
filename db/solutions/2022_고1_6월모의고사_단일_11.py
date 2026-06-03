import sympy as sp
x, k, p, q = sp.symbols('x k p q')
# 원래 방정식
eq = x**2 + k*(2*p - 3)*x - (p**2 - 2)*k + q + 2
# p=1, q=-3 대입
p_val, q_val = 1, -3
eq_substituted = eq.subs([(p, p_val), (q, q_val)])
# x=1일 때 검증
result = eq_substituted.subs(x, 1)
result_simplified = sp.simplify(result)
if result_simplified == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')