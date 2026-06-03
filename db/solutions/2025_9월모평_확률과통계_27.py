from fractions import Fraction
p0 = Fraction(1, 6)
p1 = Fraction(1, 4)
p2 = p0
p3 = p1
p4 = p0
# 조건 검증
assert p0 == p2, 'P(X=0)!=P(X=2)'
assert p1 == p3, 'P(X=1)!=P(X=3)'
assert p2 == p4, 'P(X=2)!=P(X=4)'
# 합=1
total = p0+p1+p2+p3+p4
assert total == Fraction(1,1), f'sum={total}'
# E(X^2)=35/6
EX2 = 0**2*p0 + 1**2*p1 + 2**2*p2 + 3**2*p3 + 4**2*p4
assert EX2 == Fraction(35,6), f'E(X^2)={EX2}'
print('VERIFY_PASS')