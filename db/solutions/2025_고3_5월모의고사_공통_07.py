from sympy import symbols, diff, solve, Rational

x, k = symbols('x k')

# 원래 조건
f_prime_expr = x**2 - k*x + k - 1

# 극값 없음 조건: 판별식 = 0
discriminant = k**2 - 4*(k - 1)
k_val = solve(discriminant, k)
# k=2 확인
assert k_val == [2], f'Expected k=2, got {k_val}'

# f(x) 구성 (k=2)
from sympy import integrate
k_num = 2
f_prime = x**2 - k_num*x + k_num - 1
f_x = integrate(f_prime, x) + 2  # C=2 (f(0)=2)

# f(0)=2 검증
assert f_x.subs(x, 0) == 2, 'f(0) != 2'

# f(3) 계산
f3 = f_x.subs(x, 3)
assert f3 == 5, f'f(3) = {f3}, expected 5'

# f'(x) = (x-1)^2 >= 0 확인 (극값 없음)
from sympy import factor
factored = factor(f_prime)
assert str(factored) == '(x - 1)**2', f'f prime factored: {factored}'

print('VERIFY_PASS')