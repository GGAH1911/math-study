import sympy as sp
from sympy import symbols, diff, limit, oo, Rational

# 역함수 관계를 만족하면서 f'(2)=1/3, f(2)=2인 함수 정의
# 예: f(x) = x + (x-2)^3/36 등으로 조건 만족 가능
# 하지만 검증은 조건으로부터의 논리적 도출 확인

f2 = 2
fp2 = Rational(1, 3)
g2 = 2  # f와 g가 역함수이므로
gp2 = 1 / fp2  # 역함수 미분 규칙

# h'(2) 계산
h_prime_2 = (gp2 * f2 - g2 * fp2) / (f2**2)

if h_prime_2 == Rational(4, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')