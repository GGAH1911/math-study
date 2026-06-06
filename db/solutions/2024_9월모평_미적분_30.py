import numpy as np
from scipy.optimize import fsolve

# θ = π/4일 때 φ 찾기
def tan_theta_eq(phi):
    return 5 * np.sin(phi) / (5 * np.cos(phi) + 1) - 1

phi_val = fsolve(tan_theta_eq, 0.93)[0]
print(f'φ at θ=π/4: {phi_val:.6f}')
print(f'cos φ = {np.cos(phi_val):.6f}, sin φ = {np.sin(phi_val):.6f}')

# 수치 미분으로 확인
def S_phi(phi):
    return 25 * np.sin(phi) * np.cos(phi) + 5 * np.sin(phi)

def theta_of_phi(phi):
    return np.arctan(5 * np.sin(phi) / (5 * np.cos(phi) + 1))

# φ에서의 미분값
dphi = 1e-8
dS_dphi = (S_phi(phi_val + dphi) - S_phi(phi_val - dphi)) / (2 * dphi)
dtheta_dphi = (theta_of_phi(phi_val + dphi) - theta_of_phi(phi_val - dphi)) / (2 * dphi)

print(f'dS/dφ = {dS_dphi:.6f}')
print(f'dθ/dφ = {dtheta_dphi:.6f}')

dS_dtheta = dS_dphi / dtheta_dphi
print(f'dS/dθ = {dS_dtheta:.6f}')
print(f'-7 × S\'(π/4) = {-7 * dS_dtheta:.1f}')

if abs(-7 * dS_dtheta - 32) < 0.1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')