from math import comb

# 이항정리: (x+2)^5에서 x^3의 계수
# x^k의 계수 = C(5,k) * 2^(5-k)
k = 3
coeff = comb(5, k) * (2 ** (5 - k))
print(f'Computed coefficient: {coeff}')

# 검증: (x+2)^5를 전개해서 x^3 계수 확인
import sympy as sp
x = sp.Symbol('x')
expr = (x + 2) ** 5
expanded = sp.expand(expr)
coeff_x3 = expanded.coeff(x, 3)

if coeff_x3 == 40:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')