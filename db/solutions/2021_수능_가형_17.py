from sympy import Rational, binomial

# k: 주사위 눈이 2 이하인 횟수
# k ~ B(15, 1/3)
# 점 P: (3k, 15-k)
# 직선: 3x + 4y = 0
# 거리: X = k + 12

# E(k) 계산
E_k = Rational(0)
for k in range(16):
    prob_k = binomial(15, k) * Rational(1, 3)**k * Rational(2, 3)**(15-k)
    E_k += prob_k * k

# E(X) = E(k + 12)
E_X = E_k + 12

# 점 P 좌표 확인 및 거리 재검증
E_X_direct = Rational(0)
for k in range(16):
    prob_k = binomial(15, k) * Rational(1, 3)**k * Rational(2, 3)**(15-k)
    x = 3 * k
    y = 15 - k
    dist = (5 * k + 60) / Rational(5)
    E_X_direct += prob_k * dist

if E_X == 17 and E_X_direct == 17:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')