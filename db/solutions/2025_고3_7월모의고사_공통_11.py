from sympy import symbols, Rational, diff, solve, Abs, Min

t = symbols('t', real=True, nonneg=True)
x1 = t**3 - 5*t**2 + 10*t
x2 = Rational(5,2)*t**2 - 2*t - 10

f = x1 - x2  # = t^3 - 15/2*t^2 + 12t + 10

# 임계점 찾기
fp = diff(f, t)
critical = solve(fp, t)
print('임계점:', critical)

# t=4에서 f값 (거리 최소 확인)
f_at_4 = f.subs(t, 4)
print('f(4) =', f_at_4)  # should be 2 > 0

# t=4 전후에서 f'의 부호 (t=4이 극소 확인)
print('f\' (t=3) =', fp.subs(t, 3))  # negative
print('f\' (t=5) =', fp.subs(t, 5))  # positive

# t=4에서 f값이 t=1에서의 f값보다 작은지 확인
f_at_1 = f.subs(t, 1)
print('f(1) =', f_at_1)
print('min distance at t=4:', f_at_4 < f_at_1)

# 점 P의 가속도 = x1''
acc_P = diff(x1, t, 2)
acc_at_4 = acc_P.subs(t, 4)
print('P의 가속도 at t=4:', acc_at_4)

if acc_at_4 == 14:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
