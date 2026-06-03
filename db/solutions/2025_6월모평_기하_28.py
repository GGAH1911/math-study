import numpy as np

A = np.array([1.0, 0.0])
B = np.array([1.0, 1.0])
answer_value = 12/5

best_pq = float('inf')
best_result = None
N = 8000

for theta in np.linspace(0, 2*np.pi, N, endpoint=False):
    P = np.array([np.cos(theta), np.sin(theta)])
    if np.linalg.norm(P - A) < 1e-9:
        continue
    M = (P + A) / 2
    AP_vec = P - A
    direction = np.array([-AP_vec[1], AP_vec[0]])
    direction /= np.linalg.norm(direction)
    MB = M - B
    b_coef = 2 * np.dot(MB, direction)
    c_coef = np.dot(MB, MB) - 9
    disc = b_coef**2 - 4 * c_coef
    if disc < 0:
        continue
    for sign in [1, -1]:
        t = (-b_coef + sign * np.sqrt(disc)) / 2
        Q = M + t * direction
        # Check ORIGINAL conditions from problem
        if abs(np.linalg.norm(P) - 1) > 1e-7:
            continue
        if abs(np.linalg.norm(Q - B) - 3) > 1e-7:
            continue
        AP = P - A
        QA = A - Q
        QP = P - Q
        dot_cond = np.dot(AP, QA + QP)
        if abs(dot_cond) > 1e-6:
            continue
        if np.linalg.norm(AP) < 1e-9:
            continue
        pq = np.linalg.norm(P - Q)
        if pq < best_pq - 1e-10:
            best_pq = pq
            best_result = float(np.dot(AP, Q - B))

print(f'min |PQ| = {best_pq}')
print(f'AP . BQ  = {best_result}')
print(f'expected = {answer_value}')
if best_result is not None and abs(best_result - answer_value) < 1e-3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
