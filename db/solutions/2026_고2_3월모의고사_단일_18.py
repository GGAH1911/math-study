import sympy as sp

# 원래 함수
x, t = sp.symbols('x t', real=True)
f = x**2 - 6*x + 5
f_t = t**2 - 6*t + 5

# 원래 방정식의 근 구하기
eq1 = f
eq2_expr = f + sp.Rational(1, 3) * f_t

# t = -1일 때
roots_t_minus1_eq1 = sp.solve(eq1, x)
roots_t_minus1_eq2 = sp.solve(eq2_expr.subs(t, -1), x)
all_roots_t_minus1 = list(set(roots_t_minus1_eq1 + roots_t_minus1_eq2))

# t = 7일 때
roots_t_7_eq1 = sp.solve(eq1, x)
roots_t_7_eq2 = sp.solve(eq2_expr.subs(t, 7), x)
all_roots_t_7 = list(set(roots_t_7_eq1 + roots_t_7_eq2))

# t = 0일 때 (다른 값)
roots_t_0_eq1 = sp.solve(eq1, x)
roots_t_0_eq2 = sp.solve(eq2_expr.subs(t, 0), x)
all_roots_t_0 = list(set(roots_t_0_eq1 + roots_t_0_eq2))

verify = len(all_roots_t_minus1) == 3 and len(all_roots_t_7) == 3 and len(all_roots_t_0) == 4

# f(10) 확인
f_10 = 10**2 - 6*10 + 5
verify = verify and f_10 == 45

print('VERIFY_PASS' if verify else 'VERIFY_FAIL')