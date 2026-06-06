import sympy as sp

# 원래 문제의 함수와 조건
f = lambda x: 3*x**2 + 2*x

# 조건 1: f(1) = 5
cond1 = f(1) == 5
print(f'f(1) = {f(1)}, 조건 1 (f(1)=5): {"PASS" if cond1 else "FAIL"}')

# 조건 2: 적분 조건 확인
x_sym = sp.Symbol('x', real=True)
t = sp.Symbol('t', real=True)

# f(t) = 3t^2 + 2t
f_t = 3*t**2 + 2*t

# 좌변: ∫₀ˣ f(t)dt
L = sp.integrate(f_t, (t, 0, x_sym))

# 우변: 2x³ + ∫₀⁻ˣ f(t)dt
R = 2*x_sym**3 + sp.integrate(f_t, (t, 0, -x_sym))

# 조건 검증 (정리)
L_simplified = sp.expand(L)
R_simplified = sp.expand(R)
cond2 = sp.simplify(L_simplified - R_simplified) == 0
print(f'적분 조건 $\\int_0^x f(t)dt = 2x^3 + \\int_0^{{-x}} f(t)dt$: {"PASS" if cond2 else "FAIL"}')

# 최종 답 f(2)
result = f(2)
print(f'\nf(2) = {result}')
print('VERIFY_PASS' if (cond1 and cond2) else 'VERIFY_FAIL')