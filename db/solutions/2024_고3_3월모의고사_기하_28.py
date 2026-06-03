import numpy as np

# 확정 파라미터
c = 6
a1 = 9
b1 = np.sqrt(45)
F  = np.array([6.0, 0.0])
Fp = np.array([-6.0, 0.0])  # F'
A  = np.array([6.0, 5.0])
P  = np.array([9.0, 0.0])

# cos(∠FF'A) = 12/13 검증
v1 = F - Fp; v2 = A - Fp
cos_check = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
assert abs(cos_check - 12/13) < 1e-10, 'cos check fail'

# C2 장축
two_a2 = np.linalg.norm(P - F) + np.linalg.norm(P - A)  # 3 + sqrt(34)

# C1을 매개변수화하여 C2와의 교점 탐색
ts = np.linspace(0, 2*np.pi, 500000)
xs = a1 * np.cos(ts)
ys = b1 * np.sin(ts)
cvals = np.sqrt((xs-6)**2 + ys**2) + np.sqrt((xs-6)**2 + (ys-5)**2) - two_a2
sign_changes = np.where(np.diff(np.sign(cvals)))[0]

found = False
for idx in sign_changes:
    t1, t2 = ts[idx], ts[idx+1]
    for _ in range(80):
        tm = (t1 + t2) / 2
        x, y = a1*np.cos(tm), b1*np.sin(tm)
        val = np.sqrt((x-6)**2+y**2) + np.sqrt((x-6)**2+(y-5)**2) - two_a2
        ref = np.sqrt((a1*np.cos(t1)-6)**2+(b1*np.sin(t1))**2) + np.sqrt((a1*np.cos(t1)-6)**2+(b1*np.sin(t1)-5)**2) - two_a2
        if val * ref < 0: t2 = tm
        else: t1 = tm
    xq, yq = a1*np.cos((t1+t2)/2), b1*np.sin((t1+t2)/2)
    if abs(xq-9) < 0.01 and abs(yq) < 0.01: continue  # skip P
    Q = np.array([xq, yq])
    FpQ = np.linalg.norm(Q - Fp)
    AQ  = np.linalg.norm(Q - A)
    diff = FpQ - AQ
    expected = 15 - np.sqrt(34)
    if abs(diff - expected) < 1e-5:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: diff={diff:.8f}, expected={expected:.8f}')
    found = True
    break

if not found:
    print('VERIFY_FAIL: Q not found')
