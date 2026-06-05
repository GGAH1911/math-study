from sympy import Rational, symbols, summation, limit, oo

# 기호 정의
k = symbols('k', integer=True, positive=True)
n_sym = symbols('n', integer=True, positive=True)

# 좌변의 합: sum(2k^2 - 3, k=1..n)
lower_sum = summation(2*k**2 - 3, (k, 1, n_sym))

# 우변의 합: sum(2k^2 + 4, k=1..n)
upper_sum = summation(2*k**2 + 4, (k, 1, n_sym))

# 극한 계산
lower_limit = limit(lower_sum / n_sym**3, n_sym, oo)
upper_limit = limit(upper_sum / n_sym**3, n_sym, oo)

# 예상 답
answer = Rational(2, 3)

# 검증: 샌드위치 정리
if lower_limit == answer and upper_limit == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')