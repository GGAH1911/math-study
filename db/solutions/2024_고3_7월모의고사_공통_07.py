import sympy as sp

x, a = sp.symbols('x a')
f = x**3 - 3*x + 2*a

# a = 5를 찾기 위해 극솟값 조건 사용
# f'(x) = 3x^2 - 3
f_prime = sp.diff(f, x)
crit_points = sp.solve(f_prime, x)

# x=1에서 극솟값, 값이 a+3이어야 함
f_at_1 = f.subs(x, 1)
eq = sp.Eq(f_at_1, a + 3)
a_val = sp.solve(eq, a)[0]

# a=5일 때 극댓값 계산
f_func = x**3 - 3*x + 2*a_val
f_at_minus1 = f_func.subs(x, -1)

# 검증
if f_at_minus1 == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')