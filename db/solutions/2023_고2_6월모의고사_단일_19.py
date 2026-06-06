from sympy import *

def solve(angle_COB_factor=2, eval_point1=pi/16, eval_point2=pi/8):
    """
    반원 문제의 완전 파라미터 솔버
    
    Parameters:
    - angle_COB_factor: ∠COB = angle_COB_factor × ∠CAB (기본값 2)
      원본 문제에서 ∠COB = 2θ, ∠CAB = θ이므로 angle_COB_factor = 2
    - eval_point1: f(θ)를 계산할 각도 (기본값 π/16)
    - eval_point2: g(θ)를 계산할 각도 (기본값 π/8)
    
    Returns:
    - 최종 답: p × f(eval_point1) × g(eval_point2)
    """
    theta = symbols('theta', real=True, positive=True)
    
    # Q = (1 + cos(2·angle_COB_factor·θ), sin(2·angle_COB_factor·θ))
    # D = (1, 0)
    # |QD|² = cos²(2·angle_COB_factor·θ) + sin²(2·angle_COB_factor·θ) = 1
    Q_x = 1 + cos(2 * angle_COB_factor * theta)
    Q_y = sin(2 * angle_COB_factor * theta)
    D_x = 1
    D_y = 0
    
    QD_squared = (Q_x - D_x)**2 + (Q_y - D_y)**2
    QD_squared_simplified = simplify(QD_squared)
    p = sqrt(QD_squared_simplified)
    p = simplify(p)  # p = 1 (기하학적 필연)
    
    # f(θ) = ∠QDB = 2·angle_COB_factor·θ
    # 원본: ∠COB = 2θ이므로 f(θ) = 4θ
    f_theta = 2 * angle_COB_factor * theta
    f_eval = f_theta.subs(theta, eval_point1)
    f_eval = simplify(f_eval)
    
    # g(θ) = 2cos(angle_COB_factor·θ)
    # 원본: ∠COB = 2θ이므로 g(θ) = 2cos(2θ)
    g_theta = 2 * cos(angle_COB_factor * theta)
    g_eval = g_theta.subs(theta, eval_point2)
    g_eval = simplify(g_eval)
    
    # 최종 답
    final_answer = p * f_eval * g_eval
    final_answer = simplify(final_answer)
    
    return final_answer

# 원본 문제 검증
CANDIDATE = solve()

# 예상 답: π√2/4
expected = pi * sqrt(2) / 4

if simplify(CANDIDATE - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')