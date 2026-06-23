from scipy.integrate import quad
import numpy as np

# Define f(x) = (4/3)*x - 4
def f(x):
    return (4/3)*x - 4

# Verify condition (가): f(x) = f(x-3) + 4
test_x = np.linspace(0, 10, 100)
for x in test_x:
    val1 = f(x)
    val2 = f(x-3) + 4
    if not np.isclose(val1, val2):
        print('VERIFY_FAIL')
        exit()

# Verify condition (나): ∫₀⁶ f(x)dx = 0
integral_0_6, _ = quad(f, 0, 6)
if not np.isclose(integral_0_6, 0):
    print('VERIFY_FAIL')
    exit()

# Calculate area from x=6 to x=9
area, _ = quad(lambda x: abs(f(x)), 6, 9)

if np.isclose(area, 18):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')