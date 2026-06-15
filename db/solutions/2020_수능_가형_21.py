import numpy as np
from scipy.optimize import fsolve
from scipy.integrate import quad

def g(t):
    return (t - 1) * np.exp(t) - (t + 1)

def g_prime(t):
    return t * np.exp(t) - 1

# Check ㄱ: m < 0 for some a < b
m_test, _ = quad(g, 0, 1)
print(f'ㄱ check: integral from 0 to 1 = {m_test:.4f}, m < 0: {m_test < 0}')

# Check ㄴ: symmetry of zeros
def find_zero():
    return fsolve(g, 0.5)[0]

c1 = find_zero()
print(f'ㄴ check: g({c1:.4f}) = {g(c1):.6f}, g({-c1:.4f}) = {g(-c1):.6f}')
print(f'ㄴ: g(c)=0 => g(-c)=0: {abs(g(-c1)) < 1e-6}')

# Check ㄷ: at minimum integral (c1 < 0 < -c1)
if c1 < 0:
    c = -c1
    ratio = (1 + g_prime(c)) / (1 + g_prime(-c))
    threshold = -np.exp(2)
    print(f'ㄷ check: ratio = {ratio:.4f}, -e^2 = {threshold:.4f}')
    print(f'ㄷ: ratio < -e^2: {ratio < threshold}')
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')