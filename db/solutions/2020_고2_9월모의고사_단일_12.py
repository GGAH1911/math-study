import sympy as sp

t = sp.Symbol('t', real=True)

# f(t) = t² - 4t + 5의 최솟값을 [-1, 1]에서 구하기
f = t**2 - 4*t + 5
f_prime = sp.diff(f, t)

# 임계점: t = 2 (구간 밖)
# 끝점에서의 값
f_at_minus1 = f.subs(t, -1)
f_at_1 = f.subs(t, 1)

min_f = min(f_at_minus1, f_at_1)
k_max = min_f / 5

# 검증: k = 2/5일 때 부등식이 항상 성립하는지 확인
k = sp.Rational(2, 5)
lhs = t**2 - 4*t - 5*k + 5
lhs = sp.expand(lhs)

# t ∈ [-1, 1]에서 최솟값
lhs_at_minus1 = lhs.subs(t, -1)
lhs_at_1 = lhs.subs(t, 1)

min_lhs = min(lhs_at_minus1, lhs_at_1)

if min_lhs >= 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')