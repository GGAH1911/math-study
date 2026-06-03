from fractions import Fraction

# 원래 문제 조건:
# - 과수원 A: 평균 11, 분산 5/3
# - 과수원 B의 6개 당도: 11, 9, 12, 9, a, a+1
# - B의 평균 = A의 평균 = 11
# - B의 분산 = b
# - A가 더 고르다(=A의 분산 < B의 분산)
# - 답: a + b = 43/3

claimed_sum = Fraction(43, 3)
A_mean = Fraction(11)
A_var = Fraction(5, 3)

# 평균 조건으로 a 결정
# (11 + 9 + 12 + 9 + a + (a+1)) / 6 = 11
# (42 + 2a) / 6 = 11  =>  a = 12
from sympy import symbols, Eq, solve, Rational
a_sym = symbols('a', real=True)
fixed = [11, 9, 12, 9]
B_values_expr = fixed + [a_sym, a_sym + 1]
mean_eq = Eq(sum(B_values_expr) / 6, 11)
a_sol = solve(mean_eq, a_sym)
assert len(a_sol) == 1, 'unique a 필요'
a = Rational(a_sol[0])

# 분산 b 계산 (원래 조건: B의 분산을 직접 정의대로 계산)
B_values = [Rational(v) if not hasattr(v,'subs') else Rational(v.subs(a_sym, a)) for v in [11,9,12,9,a, a+1]]
B_mean = sum(B_values) / 6
assert B_mean == Rational(11), f'B mean must equal A mean: got {B_mean}'
b = sum((x - B_mean)**2 for x in B_values) / 6

# 'A가 더 고르다' 조건: A의 분산 < B의 분산
assert Rational(5,3) < b, f'A가 더 고르다 조건 위배: A_var={Rational(5,3)}, B_var={b}'

# a, b가 양수(또는 상수)인지
assert a > 0 and b > 0

# 최종 비교
result = Rational(a) + b
if result == Rational(43, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', result)
