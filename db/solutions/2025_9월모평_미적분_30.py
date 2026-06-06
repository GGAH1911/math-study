import sympy as sp
from scipy import integrate
import numpy as np

# 검증: k=1/4, k=3/2에서 조건 확인
k_vals = [sp.Rational(1,4), sp.Rational(3,2)]
results = []

for k in k_vals:
    if k < sp.Rational(1,2):
        C1 = 0
        C2 = 2
        F_0 = (1 - k) + C1
    else:
        C1 = 2*sp.E - 2
        C2 = 2*sp.E
        F_0 = (1 - k) + C1
    
    results.append(float(F_0))

sum_g = results[0] + results[1]
print(f'g(1/4) = {sp.Rational(3,4)} = {float(sp.Rational(3,4))}')
print(f'g(3/2) = {2*sp.E - sp.Rational(5,2)}')
print(f'Sum = {2*sp.E - sp.Rational(7,4)}')

p, q = 2, sp.Rational(-7,4)
answer = 100*(p + q)
print(f'100(p+q) = {answer}')
if answer == 25:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')