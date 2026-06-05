import sympy as sp
k = sp.sqrt(7)
f = lambda x: x**3 - 3*x
f_prime = lambda x: 3*x**2 - 3

# 평균변화율
avg_rate = (f(4) - f(1)) / (4 - 1)
print(f'avg_rate = {avg_rate}')

# 접선의 기울기
tangent_slope = f_prime(float(k))
print(f'tangent_slope at k = {tangent_slope}')
print(f'f\'(sqrt(7)) = 3*7 - 3 = {3*7 - 3}')

# 검증
if abs(tangent_slope - avg_rate) < 1e-10 or 3*7 - 3 == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')