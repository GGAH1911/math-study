from sympy import *
from math import gcd

CANDIDATE = 16

x, a = symbols('x a', real=True, positive=True)

# ============================================
# PART 1: 함수 정의 및 도함수 계산
# ============================================
f = (x**2 - a*x) * exp(-x)
f_prime = diff(f, x)
f_double_prime = diff(f_prime, x)

# 형태 검증: f'(x) = -e^(-x) * (x^2 - (a+2)x + a)
f_prime_form = -exp(-x) * (x**2 - (a + 2)*x + a)
assert simplify(f_prime - f_prime_form) == 0, 'f_prime form error'

# 형태 검증: f''(x) = e^(-x) * (x^2 - (a+4)x + (2a+2))
f_double_prime_form = exp(-x) * (x**2 - (a + 4)*x + (2*a + 2))
assert simplify(f_double_prime - f_double_prime_form) == 0, 'f_double_prime form error'

# ============================================
# PART 2: a 값 결정 조건
# ============================================
# t=5가 변곡점 (f''=0의 큰 근): ((a+4) + sqrt(a^2+8))/2 = 5
# => sqrt(a^2+8) = 6 - a => a = 7/3

a_val = Rational(7, 3)

# 검증: x=5가 f''(x)=0의 근인지 확인
inflection_poly = x**2 - (a_val + 4)*x + (2*a_val + 2)
assert inflection_poly.subs(x, 5) == 0, '5 is not an inflection point'

# ============================================
# PART 3: 극값점 계산 (f'(x)=0의 근)
# ============================================
# x^2 - (a+2)x + a = 0
critical_poly = x**2 - (a_val + 2)*x + a_val
critical_roots = solve(critical_poly, x)
alpha, beta = sorted(critical_roots)

# Vieta 정리 검증: 극값점의 합 = a + 2
sum_critical = alpha + beta
assert sum_critical == a_val + 2, f'Critical sum error: {sum_critical} != {a_val + 2}'

# ============================================
# PART 4: 변곡점 확인 (제거가능 불연속)
# ============================================
inflection_roots = solve(inflection_poly, x)
# 변곡점에서는 좌극한 = 우극한 => 제거가능 불연속
# 따라서 limit_{t->k-}g(t) != limit_{t->k+}g(t)를 만족하지 않음 => 제외

# ============================================
# PART 5: 점프 불연속점은 극값점만
# ============================================
# 극값점에서만 limit_{t->k-}g(t) != limit_{t->k+}g(t)
jump_discontinuities = [alpha, beta]
sum_k = sum(jump_discontinuities)

# ============================================
# PART 6: 최종 답 계산
# ============================================
sum_rational = Rational(sum_k)
p = sum_rational.q  # 분모
q = sum_rational.p  # 분자

assert gcd(int(p), int(q)) == 1, f'Not coprime: gcd({p},{q})'

answer = p + q

if answer == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL')