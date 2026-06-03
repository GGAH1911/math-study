from math import comb

# (x+2)^7 전개식에서 x^5의 계수
# 이항정리: (x+2)^7 = sum_{k=0}^{7} C(7,k) * x^k * 2^(7-k)
# x^5의 계수는 k=5일 때: C(7,5) * 2^(7-5)

coeff = comb(7, 5) * (2 ** (7-5))
print('x^5의 계수:', coeff)

# 검증: 전개식 직접 확인
import sympy as sp
x = sp.Symbol('x')
expr = (x + 2)**7
expanded = sp.expand(expr)
coeff_x5 = expanded.coeff(x, 5)
print('검증 (sympy 전개식):', coeff_x5)

if coeff == 84 and coeff_x5 == 84:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')