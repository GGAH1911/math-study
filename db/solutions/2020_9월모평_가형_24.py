from sympy import symbols, tan, diff, pi, simplify

# 2020 9월모평 가형 24: f(x)=tan(2x) (|x|<pi/4)의 역함수 g. 100*g'(1)?
# 역함수 미분: g'(1) = 1/f'(x0), 단 f(x0)=1 → tan(2 x0)=1 → x0=pi/8.
CANDIDATE = 25
x = symbols('x')
f = tan(2 * x)
x0 = pi / 8
fp = diff(f, x).subs(x, x0)        # f'(x0) = 2 sec^2(2x0) = 4
gp1 = 1 / fp                        # g'(1) = 1/4
val = 100 * gp1
print('VERIFY_PASS' if simplify(val - CANDIDATE) == 0 else 'VERIFY_FAIL')
