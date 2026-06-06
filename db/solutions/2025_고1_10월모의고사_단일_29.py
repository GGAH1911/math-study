import sympy as sp
from sympy import sqrt, simplify, symbols, solve

# a = 3/2, h = 1
a = sp.Rational(3, 2)
h = 1

# 조건 1: (AB + BF) × SD² = 35/4
# SD² = 2a² + 2h² - 2ah
SD_sq = 2*a**2 + 2*h**2 - 2*a*h
check1 = (a + h) * SD_sq
print(f'조건 1: (a+h)×SD² = {check1}, 목표 = 35/4, 통과: {check1 == sp.Rational(35, 4)}')

# 조건 2: V₁ + V₂ = 15/4
# V₁ = a²h, V₂ = ah²
V1 = a**2 * h
V2 = a * h**2
check2 = V1 + V2
print(f'조건 2: V₁ + V₂ = {check2}, 목표 = 15/4, 통과: {check2 == sp.Rational(15, 4)}')

# a³ + h³ = 35/8 검증
check3 = a**3 + h**3
print(f'a³ + h³ = {check3}, 목표 = 35/8, 통과: {check3 == sp.Rational(35, 8)}')

# (a+h)³ = 125/8
result = (a + h)**3
print(f'(a+h)³ = {result}')
print(f'분자 q = 125, 분모 p = 8')
print(f'p + q = {8 + 125}')

if check1 == sp.Rational(35, 4) and check2 == sp.Rational(15, 4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')