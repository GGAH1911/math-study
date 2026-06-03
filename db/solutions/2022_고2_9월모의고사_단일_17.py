import sympy as sp

a = sp.Rational(3, 2)
# 원래 정의에 따라 l_n, S_n 을 그대로 계산
def l(n):
    return 3*a**n - 3*a**(n-1)
# 사다리꼴 P_n Q_n Q_{n+2} P_{n+2} 의 넓이 = shoelace
def trap_area(n):
    pts = [(n, 3*a**n), (n, 3*a**(n-1)), (n+2, 3*a**(n+1)), (n+2, 3*a**(n+2))]
    s = 0
    for i in range(4):
        x1, y1 = pts[i]
        x2, y2 = pts[(i+1) % 4]
        s += x1*y2 - x2*y1
    return sp.Abs(s) / 2

L_val = sum(l(n) for n in range(1, 21))
S_val = sum(trap_area(4*k - 3) for k in range(1, 6))
ratio = sp.simplify(S_val / L_val)
check1 = (ratio == sp.Rational(2, 5))

# 최종 답 검증
f_sqrt2 = sp.sqrt(2)**20 - 1
p = sp.Rational(3, 2)
g_20p = 20*p + 1
ans = sp.simplify(f_sqrt2 / g_20p)
check2 = (ans == 33)

print('VERIFY_PASS' if (check1 and check2) else 'VERIFY_FAIL')
