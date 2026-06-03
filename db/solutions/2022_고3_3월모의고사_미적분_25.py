from sympy import sqrt, Rational, limit, oo, symbols

n = symbols('n', positive=True, real=True)

# 극한 공식 (유리화 후): (1+a)/(2*sqrt(a)) = 5/4
# 구한 a 값들
a_values = [4, Rational(1, 4)]
target = Rational(5, 4)

all_correct = True
for a_val in a_values:
    limit_result = (1 + a_val) / (2 * sqrt(a_val))
    if limit_result != target:
        all_correct = False
        break

# 합계 검증
answer_sum = sum(a_values)
if answer_sum == Rational(17, 4) and all_correct:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')