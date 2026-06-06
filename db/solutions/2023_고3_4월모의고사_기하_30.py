import numpy as np
from scipy.optimize import fsolve

# m = 2*sqrt(6)
m = 2 * np.sqrt(6)
k = m

# 포물선과 원의 교점
# y^4 + 4y^2 - 4k^2 = 0
# u = y^2에서: u^2 + 4u - 4k^2 = 0
u = -2 + 2*np.sqrt(1 + k**2)
y_intersect = np.sqrt(u)
x_intersect = np.sqrt(1 + k**2)

# 검증 1: 교점이 포물선 위에 있는가?
parabola_check = y_intersect**2 - (2*x_intersect - 2)

# 검증 2: 교점이 원 위에 있는가?
circle_check = (x_intersect - 1)**2 + y_intersect**2 - k**2

# 검증 3: 교점이 호의 범위 내에 있는가?
x_min = 1 + k * np.sqrt(6) / 3
x_max = 1 + k
in_range = (x_intersect >= x_min - 1e-10) and (x_intersect <= x_max + 1e-10)

print(f"Parabola check (should be ~0): {parabola_check}")
print(f"Circle check (should be ~0): {circle_check}")
print(f"In range check: {in_range}")
print(f"x_min: {x_min}, x_intersect: {x_intersect}, x_max: {x_max}")

if abs(parabola_check) < 1e-8 and abs(circle_check) < 1e-8 and in_range:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")