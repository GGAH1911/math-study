import sympy as sp
import numpy as np
from scipy.optimize import fsolve

# 정수 k 값들
k_values = [-3, -2, 2, 4]

def count_solutions(k):
    """k에 대해 [0, 2π]에서 방정식의 해의 개수 계산"""
    x = sp.Symbol('x', real=True)
    
    # 두 방정식
    alpha = k / 4
    beta = (3*k - k**2) / 4
    
    solutions = set()
    
    # sin x = alpha의 해를 찾음
    if -1 <= alpha <= 1:
        if alpha == 0:
            sols_alpha = [0, np.pi, 2*np.pi]
        elif alpha == 1:
            sols_alpha = [np.pi/2]
        elif alpha == -1:
            sols_alpha = [3*np.pi/2]
        else:
            # 일반적인 경우
            x1 = np.arcsin(alpha)
            x2 = np.pi - x1
            sols_alpha = [x1, x2]
            if x1 < 0:
                sols_alpha = [x1 + 2*np.pi, x2]
            if x2 > 2*np.pi:
                sols_alpha = [x1, x2 - 2*np.pi]
    else:
        sols_alpha = []
    
    # sin x = beta의 해를 찾음
    if -1 <= beta <= 1:
        if beta == 0:
            sols_beta = [0, np.pi, 2*np.pi]
        elif beta == 1:
            sols_beta = [np.pi/2]
        elif beta == -1:
            sols_beta = [3*np.pi/2]
        else:
            x1 = np.arcsin(beta)
            x2 = np.pi - x1
            sols_beta = [x1, x2]
            if x1 < 0:
                sols_beta = [x1 + 2*np.pi, x2]
            if x2 > 2*np.pi:
                sols_beta = [x1, x2 - 2*np.pi]
    else:
        sols_beta = []
    
    # 모든 해를 추가 (중복 제거)
    for sol in sols_alpha:
        solutions.add(round(sol, 10))
    for sol in sols_beta:
        solutions.add(round(sol, 10))
    
    return len(solutions)

# 각 k에 대해 확인
for k in k_values:
    count = count_solutions(k)
    alpha = k / 4
    beta = (3*k - k**2) / 4
    print(f"k={k}: sin x = {alpha:.3f}, sin x = {beta:.3f} → {count} solutions")

# 조건을 만족하는 k만 세기
valid_k = [k for k in k_values if count_solutions(k) == 2]
if len(valid_k) == 4:
    product = 1
    for k in valid_k:
        product *= k
    if product == 48:
        print("\nVERIFY_PASS")
    else:
        print("\nVERIFY_FAIL")
else:
    print("\nVERIFY_FAIL")