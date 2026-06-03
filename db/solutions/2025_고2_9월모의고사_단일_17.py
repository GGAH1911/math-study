import sympy as sp
from sympy import symbols, sqrt, limit, simplify

t = symbols('t', real=True, positive=True)

# 삼각형 APQ의 넓이: A(1,1), P(t, t^2), Q(t, sqrt(t))
# PQ의 길이 = t^2 - sqrt(t), 높이 = t - 1
S_t = (1/2) * (t**2 - sqrt(t)) * (t - 1)

# 극한값 계산
result = limit(S_t / (t - 1)**2, t, 1, '+')
print(f'Result: {result}')
print(f'Result as float: {float(result)}')

# 검증: 3/4와 일치하는지 확인
if simplify(result - sp.Rational(3, 4)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')