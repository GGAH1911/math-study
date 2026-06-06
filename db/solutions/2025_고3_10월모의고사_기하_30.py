import numpy as np

# 좌표 설정
A = np.array([0.0, 0.0])
B = np.array([8.0, 0.0])
C = np.array([8.0, 8.0])
D = np.array([0.0, 8.0])
E = np.array([-4.0, 8.0])

# 원의 중심과 반지름
center = np.array([8.0, 4.0])
radius = 4.0

def compute_ae_dot_aq(theta):
    # 점 P
    p = center + radius * np.array([np.cos(theta), np.sin(theta)])
    ap = p - A
    ae = E - A
    ae_dot_ap = np.dot(ae, ap)
    
    # 조건에 따라 Q 결정
    if ae_dot_ap >= 0:
        # Case 1: Q = 2P - (B+C)/2
        q = 2*p - (B + C)/2
    else:
        # Case 2: Q = 3P/2 - (B+C)/4
        q = 3*p/2 - (B + C)/4
    
    aq = q - A
    ae_dot_aq = np.dot(ae, aq)
    return ae_dot_aq

# 여러 각도에서 값 계산
thetas = np.linspace(0, 2*np.pi, 10000)
values = np.array([compute_ae_dot_aq(theta) for theta in thetas])

M = np.max(values)
m = np.min(values)
result = (M + m)**2

print(f'M = {M:.6f}')
print(f'm = {m:.6f}')
print(f'M + m = {M + m:.6f}')
print(f'(M + m)^2 = {result:.1f}')

# 이론적 값과 비교
theory_M = 32 * np.sqrt(5)
theory_m = -24 * np.sqrt(5)
theory_result = (8 * np.sqrt(5))**2

print(f'\nTheoretical M = {theory_M:.6f}')
print(f'Theoretical m = {theory_m:.6f}')
print(f'Theoretical (M + m)^2 = {theory_result:.1f}')

if abs(result - 320) < 1:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')