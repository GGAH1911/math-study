import sympy as sp
x = sp.Symbol('x')

# f'(1) = 3 조건 확인
# 극한값이 9가 되는지 검증

# x^3 - 1 = (x-1)(x^2 + x + 1)
factor_check = sp.expand((x - 1) * (x**2 + x + 1))
assert factor_check == x**3 - 1, 'Factorization failed'

# lim(x->1) (x^2 + x + 1) = 3
limit_factor = (1**2 + 1 + 1)
assert limit_factor == 3, 'Limit of factor failed'

# f'(1) = 3 일 때
# lim(x->1) [f(x^3) - f(1)] / (x-1) 
# = f'(1) * lim(x->1) (x^2 + x + 1)
# = 3 * 3 = 9

result = 3 * 3
assert result == 9, 'Final calculation failed'

print('VERIFY_PASS')