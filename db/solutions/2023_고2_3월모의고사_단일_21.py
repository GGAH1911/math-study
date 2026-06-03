import numpy as np

# Problem setup
# Arc C: x^2+y^2=25, x<=0, y>=0  => theta in [pi/2, pi]
# A=(4,2), centroid condition => Q = (-4-a, -2-b)
# A' = (-4,-2)

thetas = np.linspace(np.pi/2, np.pi, 10000)
a = 5*np.cos(thetas)
b = 5*np.sin(thetas)
Qx = -4 - a
Qy = -2 - b
Ap = np.array([-4.0, -2.0])

# Check ㄱ: midpoint of PQ = (-2, -1) always
mid_x = (a + Qx) / 2
mid_y = (b + Qy) / 2
assert np.allclose(mid_x, -2.0, atol=1e-9) and np.allclose(mid_y, -1.0, atol=1e-9), 'ㄱ FAIL'

# Check ㄴ: |A'Q| = 5 always
AQ_len = np.sqrt((Qx - Ap[0])**2 + (Qy - Ap[1])**2)
assert np.allclose(AQ_len, 5.0, atol=1e-9), 'ㄴ FAIL'

# Check ㄷ: area of triangle A'QP and M*m
# Shoelace formula
area = 0.5 * np.abs(
    Ap[0]*(Qy - b) + Qx*(b - Ap[1]) + a*(Ap[1] - Qy)
)
M = area.max()
m = area.min()
Mm = M * m

expected_Mm = 20 * np.sqrt(5)  # claim in ㄷ
my_Mm = 25 * np.sqrt(5)        # my calculation

assert abs(Mm - my_Mm) < 0.01, f'M*m = {Mm:.6f}, expected 25sqrt5 = {my_Mm:.6f}'
assert abs(Mm - expected_Mm) > 0.1, 'ㄷ wrongly TRUE'

# All checks: ㄱ TRUE, ㄴ TRUE, ㄷ FALSE => answer is ② (ㄱ,ㄴ)
print('VERIFY_PASS')
