import sympy as sp
import numpy as np
from scipy.optimize import minimize_scalar

t = sp.Symbol('t', positive=True, real=True)

# 위치 함수
x = 2*sp.sqrt(t+1)
y = t - sp.ln(t+1)

# 속도 벡터
dx_dt = sp.diff(x, t)
dy_dt = sp.diff(y, t)

# 속력 함수
v_squared = dx_dt**2 + dy_dt**2
v_squared_simplified = sp.simplify(v_squared)

# v^2의 미분
v_sq_prime = sp.diff(v_squared, t)
v_sq_prime_simplified = sp.simplify(v_sq_prime)

# 임계점 찾기
critical_points = sp.solve(v_sq_prime, t)
print(f'임계점: {critical_points}')

# t=1에서의 속력
t_min = 1
v_at_1_squared = v_squared.subs(t, t_min)
v_at_1 = sp.sqrt(v_at_1_squared)
v_at_1_simplified = sp.simplify(v_at_1)

print(f't=1에서 v^2 = {v_at_1_squared}')
print(f't=1에서 v = {v_at_1_simplified}')

# 수치 검증: 최솟값 확인
def v_numeric(t_val):
    return float(sp.sqrt((1/sp.sqrt(t_val+1))**2 + (t_val/(t_val+1))**2))

result = minimize_scalar(v_numeric, bounds=(0.01, 10), method='bounded')
print(f'수치 최솟값: t={result.x:.6f}, v={result.fun:.10f}')
print(f'√3/2의 값: {float(sp.sqrt(3)/2):.10f}')

if abs(result.fun - float(sp.sqrt(3)/2)) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')