from fractions import Fraction

p1 = Fraction(5, 16)
p2 = Fraction(1, 2) - p1
p3 = p1 - Fraction(1, 4)
p4 = p2 + Fraction(1, 4)

# 조건 1: k=1
cond1 = (p3 - p1 == Fraction(-1, 4))
# 조건 2: k=2
cond2 = (p4 - p2 == Fraction(1, 4))
# 확률 합
cond3 = (p1 + p2 + p3 + p4 == 1)
# 기댓값
EX = 1*p1 + 2*p2 + 3*p3 + 4*p4
cond4 = (EX == Fraction(21, 8))
# 모든 확률 비음수
cond5 = all(p >= 0 for p in [p1, p2, p3, p4])

if cond1 and cond2 and cond3 and cond4 and cond5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'cond1={cond1}, cond2={cond2}, cond3={cond3}, cond4={cond4}, cond5={cond5}')
