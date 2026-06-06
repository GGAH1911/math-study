from sympy import *
p, m, q = 3, 2, -5

# f(x) + g(m) = -4 검증
f_m = Rational(1,2) * (m - p)**2 + q
g_m = -Rational(1,2) * (0 - p)**2 - q
sum_check = f_m + g_m
print('f(m) + g(m) =', sum_check, '(expect -4)')
assert sum_check == -4, f'VERIFY_FAIL: {sum_check} != -4'

# f(x) = g(x)의 근 확인
x = symbols('x')
eq = Eq(Rational(1,2)*(x-p)**2 + q, -Rational(1,2)*(x-m-p)**2 - q)
roots = solve(eq, x)
alpha, beta = min(roots), max(roots)
print(f'α = {alpha}, β = {beta}')
assert alpha == 1 and beta == 7, 'VERIFY_FAIL: roots mismatch'
assert alpha + beta == m + 2*p, 'VERIFY_FAIL: sum property'

# h(x) = t에서 t=4인 경우 4개 근의 합이 4p+2m인지 확인
t = 4
roots_f = solve(Rational(1,2)*(x-p)**2 + q - t, x)
roots_g = solve(-Rational(1,2)*(x-m-p)**2 - q - t, x)
print(f'f(x)={t}의 근:', roots_f)
print(f'g(x)={t}의 근:', roots_g)
all_roots_in_range = [r for r in roots_f if r <= alpha or r >= beta] + [r for r in roots_g if alpha < r < beta]
total_sum = sum(all_roots_in_range)
expected_sum = 4*p + 2*m
print(f'실근의 합: {total_sum} (expect {expected_sum})')
assert simplify(total_sum - expected_sum) == 0, 'VERIFY_FAIL'
print('VERIFY_PASS')