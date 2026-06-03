import sympy as sp

a = 4
b = sp.pi / 12
x = sp.Symbol('x')
f = a - sp.sqrt(3) * sp.tan(2*x)

# 원래 함수에 직접 대입
f_left = sp.simplify(f.subs(x, -sp.pi/6))   # 최댓값 = 7?
f_right = sp.simplify(f.subs(x, b))          # 최솟값 = 3?

# 구간 내 단조감소 확인: 도함수 = -2sqrt(3)*sec^2(2x) < 0
df = sp.diff(f, x)
df_check = sp.simplify(df.subs(x, 0))  # 대표점에서 음수인지

cond1 = sp.Eq(f_left, 7)
cond2 = sp.Eq(f_right, 3)
cond3 = df_check < 0

if sp.simplify(f_left - 7) == 0 and sp.simplify(f_right - 3) == 0 and bool(cond3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('f(-pi/6) =', f_left)
    print('f(pi/12) =', f_right)
    print('df at 0 =', df_check)
