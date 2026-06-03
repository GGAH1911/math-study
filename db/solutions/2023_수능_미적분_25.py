import sympy as sp
import numpy as np

# 극한 조건: lim(a_n / (3^n + 2^(2n-1))) = 3
# 등비수열 a_n = a_1 * r^(n-1)

a_1, r, n = sp.symbols('a_1 r n', real=True, positive=True)

# 정해진 값
a_1_val = 6
r_val = 4

# a_n 정의
def a_n_func(n_val, a1, r_coef):
    return a1 * (r_coef ** (n_val - 1))

# 극한 검증
results = []
for n_val in [10, 50, 100, 200]:
    numerator = a_n_func(n_val, a_1_val, r_val)
    denominator = 3**n_val + 2**(2*n_val - 1)
    limit_approx = numerator / denominator
    results.append(limit_approx)

print(f"극한값 근사 (n=10, 50, 100, 200): {[float(x) for x in results[:4]]}")

# 정확한 극한 계산 (sympy)
n_var = sp.Symbol('n', integer=True, positive=True)
a_n_expr = a_1_val * r_val**(n_var - 1)
denominator_expr = 3**n_var + 2**(2*n_var - 1)

# n->∞일 때 극한
fraction = a_n_expr / denominator_expr
limit_exact = sp.limit(fraction, n_var, sp.oo)

print(f"극한값 (정확): {limit_exact}")
print(f"극한값 == 3: {limit_exact == 3}")

# a_2 계산
a_2 = a_1_val * r_val
print(f"a_2 = {a_2}")

if abs(float(limit_exact) - 3.0) < 1e-10:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")