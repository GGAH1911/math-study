import numpy as np
from scipy.optimize import fsolve

def equations(vars):
    a, b = vars
    eq1 = a**3 + b**3 - 12
    eq2 = a**2 + b**2 - a*b - 4
    return [eq1, eq2]

sol = fsolve(equations, [2.0, 1.0])
a, b = sol

A = np.array([a*np.sqrt(2)/2, 0, a/np.sqrt(2)])
B = np.array([0, a*np.sqrt(2)/2, a/np.sqrt(2)])
F = np.array([0, b*np.sqrt(2)/2, b/np.sqrt(2)])
E = np.array([b*np.sqrt(2)/2, 0, b/np.sqrt(2)])

AF_len = np.linalg.norm(F - A)
print(f'AF length: {AF_len}, expected: 2')

AB = B - A
AF = F - A
AE = E - A

cross_AB_AF = np.cross(AB, AF)
cross_AF_AE = np.cross(AF, AE)

S_ABF = 0.5 * np.linalg.norm(cross_AB_AF)
S_AFE = 0.5 * np.linalg.norm(cross_AF_AE)
S = S_ABF + S_AFE

result = 32 * S**2
print(f'32*S^2 = {result}')

if abs(result - 126) < 0.01:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')