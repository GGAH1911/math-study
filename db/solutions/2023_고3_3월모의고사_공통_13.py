import sympy as sp

a = sp.Rational(1, 2)
b = sp.Rational(-1, 2)
t = sp.Symbol('t', real=True)

def f(val): return val**2 + a*val + b
def g(val): return sp.sin(val)

# 조건 (가) 검증
cond_ga = sp.simplify((g(a * sp.pi))**2 - 1) == 0

# f(t)=0 의 근
roots = sp.solve(f(t), t)

# 각 근에 대해 [0, 2π]에서 sin x = root 의 해 합 계산
# root = 1/2: x = π/6, 5π/6  →  합 = π
# root = -1:  x = 3π/2       →  합 = 3π/2
sum_x = sp.pi/6 + sp.Rational(5,1)*sp.pi/6 + sp.Rational(3,2)*sp.pi
cond_na = sp.simplify(sum_x - sp.Rational(5,2)*sp.pi) == 0

# f(2) 계산
f2 = f(2)
correct_f2 = sp.Rational(9, 2)

if cond_ga and cond_na and f2 == correct_f2:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: cond_ga={cond_ga}, cond_na={cond_na}, f(2)={f2}')
