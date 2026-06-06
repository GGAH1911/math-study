import sympy as sp
from sympy import sin, cos, limit, symbols, simplify

theta = symbols('theta', real=True, positive=True)

# f(θ) = sin(θ)/2
f = sin(theta) / 2

# 기하학적 분석으로부터 g(θ) ≈ θ³ + θ/4
g = theta**3 + theta/4

# 극한 계산
numerator = theta**3 - g
denominator = f

limit_val = limit(numerator / denominator, theta, 0)
print(f"극한값: {limit_val}")

# -k = -1/2 이므로 k = 1/2
k = sp.Rational(1, 2)
answer = 100 * k
print(f"k = {k}")
print(f"100k = {answer}")

if limit_val == -k:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")