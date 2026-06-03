from math import comb
import sympy as sp

# 이항정리로 x^9 계수 계산
k = 3
coeff = comb(5, k) * (3 ** (5 - k))

# 검증: 원래 식을 전개해서 x^9 계수 확인
x = sp.Symbol('x')
poly = (x**3 + 3)**5
expanded = sp.expand(poly)
coeff_verify = expanded.coeff(x, 9)

if coeff == 90 and coeff_verify == 90:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')