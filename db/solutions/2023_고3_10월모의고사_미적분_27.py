from sympy import Rational, symbols, simplify

# 우리 답: a=4, r=2
a, r = 4, 2

# 조건 1 검증: sum(a_n/3^n) = 4
# a_n = a*r^(n-1)이므로
# sum(a*r^(n-1)/3^n) = (a/3)*sum((r/3)^(n-1)) = a/(3-r)
condition1_value = a / (3 - r)
assert condition1_value == 4, f'조건1 실패: {condition1_value}'

# 조건 2 검증: sum(1/a_{2n})
# a_{2n} = a*r^(2n-1) = 4*2^(2n-1) = 2*4^n
# sum(1/(2*4^n)) = (1/2)*sum((1/4)^n) = (1/2)*(1/4)/(1-1/4) = (1/2)*(1/3) = 1/6
S_value = Rational(1, 2) * Rational(1, 4) / (1 - Rational(1, 4))
assert S_value == Rational(1, 6), f'S 계산 실패: {S_value}'

print('VERIFY_PASS')