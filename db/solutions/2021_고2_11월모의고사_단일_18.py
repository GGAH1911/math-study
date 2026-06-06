import sympy as sp
import numpy as np
from sympy import sqrt, symbols, limit, simplify

t = symbols('t', real=True, positive=True)

# 교점 좌표
x_A = sqrt(2*t)
y_A = 2*t
x_B = sqrt(2)
y_B = 2*t
x_C = sqrt(t+1)
y_C = t+1
x_D = sqrt(1 + 1/t)
y_D = t+1

# 삼각형 ABD 넓이
area_ABD = sp.Rational(1,2) * abs(x_A*(y_B - y_D) + x_B*(y_D - y_A) + x_D*(y_A - y_B))
area_ABD = sp.Rational(1,2) * (1-t) * (sqrt(2) - sqrt(2*t))

# 삼각형 ADC 넓이
area_ADC = sp.Rational(1,2) * (1-t) * (sqrt(1 + 1/t) - sqrt(t+1))

# 총 넓이
S = area_ABD + area_ADC
S_simplified = simplify(S)

# 극한 계산
result = limit(S / (1-t)**2, t, 1, '-')
result = simplify(result)

print(f"S(t) = {S_simplified}")
print(f"극한값 = {result}")
print(f"극한값 (수치) = {float(result):.6f}")
print(f"√2/2 = {float(sqrt(2)/2):.6f}")

if abs(float(result) - float(sqrt(2)/2)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')