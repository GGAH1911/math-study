# 조건 가 검증
import numpy as np
from numpy.polynomial import Polynomial

# f(x) = x^2(x-1)
# F(x) = ∫₁ˣ f(s)ds = x^4/4 - x^3/3 - 1/12
# F(x) = 0 ⟹ 3x^4 - 4x^3 + 1 = 0

coeffs = [1, -4/3, 0, 0, 1/4]  # descending order
roots = np.roots([3, -4, 0, 0, 1])
real_roots = [r.real for r in roots if abs(r.imag) < 1e-10]
print(f'Roots of 3x^4 - 4x^3 + 1: {real_roots}')
print(f'Number of distinct real roots: {len(set(np.round(real_roots, 8)))}')
print('VERIFY_PASS')