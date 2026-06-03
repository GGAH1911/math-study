import numpy as np

# Hyperbola: x^2/2 - y^2/2 = 1  →  x^2 - y^2 = 2
# A = (sqrt(2), 0), circle center = (-sqrt(2), 0), radius = k
# Substituting y^2 = x^2 - 2 into circle: 2x^2 + 2*sqrt(2)*x - k^2 = 0

k = 2.0 * np.sqrt(2.0)
sqrt2 = np.sqrt(2.0)

# Solve quadratic
a_c, b_c, c_c = 2.0, 2.0*sqrt2, -k**2
disc = b_c**2 - 4*a_c*c_c
x1 = (-b_c + np.sqrt(disc)) / (2*a_c)
x2 = (-b_c - np.sqrt(disc)) / (2*a_c)

points = []
count = 0
for xi in [x1, x2]:
    y2 = xi**2 - 2.0
    if y2 > 1e-9:
        points += [(xi, np.sqrt(y2)), (xi, -np.sqrt(y2))]
        count += 2
    elif abs(y2) <= 1e-9:
        points += [(xi, 0.0)]
        count += 1

# Verify each point satisfies (1) hyperbola and (2) |OA+OP|=k
all_ok = True
for px, py in points:
    if abs(px**2/2 - py**2/2 - 1) > 1e-6:
        all_ok = False
    if abs(np.sqrt((sqrt2+px)**2 + py**2) - k) > 1e-6:
        all_ok = False

if count == 3 and all_ok:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL count={count} all_ok={all_ok}')
