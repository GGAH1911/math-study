from sympy import symbols, limit, oo, simplify

x = symbols('x')
f = 2*x**2
g = x - 2
product = f * g

# 조건 (가) 검증
limit_inf = limit(product / x**3, x, oo)
print(f'조건 (가): {limit_inf}')
assert limit_inf == 2, f'조건 (가) 실패: {limit_inf}'

# 조건 (나) 검증
limit_zero = limit(product / x**2, x, 0)
print(f'조건 (나): {limit_zero}')
assert limit_zero == -4, f'조건 (나) 실패: {limit_zero}'

# f(2) 계산
f_at_2 = f.subs(x, 2)
print(f'f(2) = {f_at_2}')
assert f_at_2 == 8, f'f(2) 계산 오류'

print('VERIFY_PASS')