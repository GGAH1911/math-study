from sympy import sqrt, limit, oo, symbols, simplify, N

n = symbols('n', positive=True, integer=True)

a_n = sqrt(n*(n+2))
b_n = 2*(n+1) - 2*sqrt(n*(n+2))

product = simplify(a_n * b_n)
limit_val = limit(product, n, oo)

assert limit_val == 1, f'Expected alpha=1, got {limit_val}'

alpha = 1
f_alpha = sqrt(alpha*(alpha+2))
g_alpha = 2*(alpha+1) - 2*sqrt(alpha*(alpha+2))

result = 2*f_alpha + g_alpha
result_simplified = simplify(result)

assert result_simplified == 4, f'Expected 4, got {result_simplified}'

print('VERIFY_PASS')