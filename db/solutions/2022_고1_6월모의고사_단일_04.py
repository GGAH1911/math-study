from sympy import symbols, solve, Poly, Rational

x = symbols('x')
a, b = 1, -12

# 원래 부등식 x^2 + a*x + b < 0 의 해집합이 -4 < x < 3 인지 확인
# 방정식의 근을 구해 (-4, 3) 와 일치하는지 검사
roots = sorted(solve(x**2 + a*x + b, x))

# 이차항 계수가 양수이므로 해는 두 근 사이가 됨
expected_roots = [-4, 3]

# a - b 검증
result = a - b

if roots == expected_roots and result == 13:
    # 추가 검증: 구간 내부에서 음수, 외부에서 양수인지
    f = lambda t: t**2 + a*t + b
    if f(0) < 0 and f(-5) > 0 and f(4) > 0 and f(-4) == 0 and f(3) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')
