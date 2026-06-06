from sympy import symbols, cos, sin, series, limit, simplify, Rational, sqrt

def solve(AB=1, BC=2):
    """완전 파라미터 솔버: AB, BC를 문제 계수로 노출"""
    theta = symbols('theta', real=True, positive=True)
    
    # 좌표 설정
    # B = (0, 0), C = (BC, 0), M = (BC/2, 0), A = (AB*cos(theta), AB*sin(theta))
    
    # H는 M에서 선분 AB에 내린 수선의 발
    # AB 위의 점: s*(AB*cos(theta), AB*sin(theta)), s ∈ [0,1]
    # H = (AB*cos²(theta), AB*cos(theta)*sin(theta))
    H_x = AB * cos(theta)**2
    H_y = AB * cos(theta) * sin(theta)
    M_x = BC / 2
    M_y = 0
    
    # MH의 길이
    MH = AB * sin(theta)
    
    # D: 선분 AM 위의 점, MD = MH
    # 매개변수화: P(t) = (1-t)*M + t*A, t ∈ [0,1]
    # |P(t) - M|² = MH²에서 t_D = AB*cos(theta/2) / (2*AB*sin(theta/2))
    # 단순화: t_D = cos(theta/2)
    t_D = cos(theta/2)
    
    # E: 직선 AM과 직선 HC의 교점
    # 매개변수 t_E
    c = cos(theta)
    t_E = c / (2 - c)
    
    # 점들의 좌표
    A_x = AB * cos(theta)
    A_y = AB * sin(theta)
    C_x = BC
    C_y = 0
    
    # D의 좌표 (선분 AM 위, 매개변수 t_D)
    D_x = (1 - t_D) * M_x + t_D * A_x
    D_y = (1 - t_D) * M_y + t_D * A_y
    
    # E의 좌표 (선분 AM 위, 매개변수 t_E)
    E_x = (1 - t_E) * M_x + t_E * A_x
    E_y = (1 - t_E) * M_y + t_E * A_y
    
    # 삼각형 넓이 = (1/2)|외적|
    # 삼각형 CDE
    vec_CD_x = D_x - C_x
    vec_CD_y = D_y - C_y
    vec_CE_x = E_x - C_x
    vec_CE_y = E_y - C_y
    cross_CDE = vec_CD_x * vec_CE_y - vec_CD_y * vec_CE_x
    S = simplify(abs(cross_CDE) / 2)
    
    # 삼각형 MEH
    vec_ME_x = E_x - M_x
    vec_ME_y = E_y - M_y
    vec_MH_x = H_x - M_x
    vec_MH_y = H_y - M_y
    cross_MEH = vec_ME_x * vec_MH_y - vec_ME_y * vec_MH_x
    T = simplify(abs(cross_MEH) / 2)
    
    # 극한값 계산
    # lim_{theta->0} (S - T) / theta^3
    diff_ST = simplify(S - T)
    
    # Taylor 전개로 극한 계산
    diff_series = series(diff_ST, theta, 0, n=4)
    
    # theta³의 계수 추출
    diff_series_expanded = series(diff_ST, theta, 0, n=4)
    # (S-T) ~ (3/16)*theta³ + ... 
    # 극한값 = (S-T)/theta³의 극한 = 3/16
    
    lim_val = limit(diff_ST / theta**3, theta, 0)
    
    # 최종 답
    answer = 80 * lim_val
    
    return simplify(answer)

# 검증
CANDIDATE = 15
result = solve()

if simplify(result - CANDIDATE) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected: {CANDIDATE}, Got: {result}')