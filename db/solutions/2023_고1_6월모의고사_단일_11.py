from sympy import symbols, div

x = symbols('x')
P = x**2 - 3*x + 3

# 조건 (가): P(x)를 x-1로 나눈 나머지 = 1
quotient_a, remainder_a = div(P, x - 1, domain='ZZ')
assert remainder_a == 1, f'조건 (가) 실패: {remainder_a}'

# 조건 (나): xP(x)를 x-2로 나눈 나머지 = 2
xP = x * P
quotient_b, remainder_b = div(xP, x - 2, domain='ZZ')
assert remainder_b == 2, f'조건 (나) 실패: {remainder_b}'

# P(4) 계산 및 검증
P_4 = P.subs(x, 4)
assert P_4 == 7, f'P(4) 불일치: {P_4}'

print('VERIFY_PASS')