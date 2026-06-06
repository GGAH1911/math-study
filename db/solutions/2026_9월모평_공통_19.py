from sympy import symbols, solve, simplify
import sympy as sp

CANDIDATE = '10'

# 문제 조건 인코딩
# 주어진: f'(x) = 6x(x-a)
# 조건: 극솟값 = a (극솟값의 함수값)
# 구하는 것: 극댓값

x, a = symbols('x a', real=True)

# f'(x) = 6x(x-a)로부터 f(x) 도출 (적분)
f_prime = 6*x*(x - a)
f_integrated = sp.integrate(f_prime, x)
# f(x) = 2x^3 - 3ax^2 + c

# 문제 텍스트에서 f(a) = -a^3 + 5a라고 명시되어 있으므로, 적분상수 c = 5a
f = 2*x**3 - 3*a*x**2 + 5*a

# 극값의 위치 확인: f'(x) = 6x(x-a) = 0에서 x = 0 또는 x = a
# f''(x) = 12x - 6a이므로
# a > 0일 때: f''(0) = -6a < 0 (극대), f''(a) = 6a > 0 (극소)

# 극솟값이 a라는 조건: f(a) = a
f_at_a = f.subs(x, a)
f_at_a_simplified = simplify(f_at_a)
# f(a) = 2a^3 - 3a^3 + 5a = -a^3 + 5a

# 극솟값 조건식: f(a) = a
# -a^3 + 5a = a
# -a^3 + 4a = 0
eq_for_a = f_at_a_simplified - a
a_solutions = solve(eq_for_a, a)

# a > 0인 해만 선택
a_value = [sol for sol in a_solutions if sol > 0][0]  # a = 2

# 극댓값 계산: f(0)
f_at_0 = f.subs([(x, 0), (a, a_value)])
f_at_0_result = simplify(f_at_0)

# 최종 검증
candidate_int = int(CANDIDATE)
if f_at_0_result == candidate_int:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')