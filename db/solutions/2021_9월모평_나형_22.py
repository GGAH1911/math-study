from math import comb

# 이항정리: (x+3)^8에서 x^7의 계수
# 일반항: C(8,k) * x^k * 3^(8-k)
# k=7일 때: C(8,7) * x^7 * 3^1

k = 7
coeff = comb(8, 7) * (3 ** (8 - 7))

print(f'계수: {coeff}')

# 검증: 직접 전개로 확인
import sympy as sp
x = sp.Symbol('x')
expanded = sp.expand((x + 3) ** 8)
coeff_x7 = expanded.coeff(x, 7)

print(f'전개식에서 x^7의 계수: {coeff_x7}')

if coeff == coeff_x7 == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')