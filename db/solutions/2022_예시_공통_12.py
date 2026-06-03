from sympy import symbols, diff, solve, integrate, factor, Rational

x = symbols('x', real=True)

# g(x) = 3x - x^3 의 최댓값 (x > 0)
g = 3*x - x**3
g_prime = diff(g, x)
critical_pts = solve(g_prime, x)
positive_pts = [c for c in critical_pts if c > 0]

max_g = max(g.subs(x, c) for c in positive_pts)
k_min = max_g  # 최솟값 k

# k=2 일 때 f(x) = x^3 - 3x + 2 인수분해 확인
f = x**3 - 3*x + 2
f_factored = factor(f)  # 기대: (x-1)^2*(x+2)

# x>0 에서 f(x)>=0 확인: (x-1)^2*(x+2), x>0 이면 (x+2)>0, (x-1)^2>=0 => f>=0
# sympy 로 x>0 범위 최솟값이 0 이상인지
f_min_val = f.subs(x, 1)  # x=1 에서 최솟값 0

# k=1 (< 2) 이면 음수 구간 존재
f_k1 = x**3 - 3*x + 1
f_k1_at_1 = f_k1.subs(x, 1)  # = 1 - 3 + 1 = -1 < 0

# 적분 검증: k=2, a=0.5, b=1.5
a_val, b_val = Rational(1,2), Rational(3,2)
integral_val = integrate(x**3 - 3*x + 2, (x, a_val, b_val))

if (k_min == 2 and f_min_val == 0 and f_k1_at_1 < 0 and integral_val > 0):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
