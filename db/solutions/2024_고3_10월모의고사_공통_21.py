from sympy import symbols, Eq, solve as sp_solve

def solve(
    target_natural_count=6,     # 조건 나: g(k)≥2인 자연수 k 개수
    interval_width=4,            # (a-δ, a) 구간의 폭 (δ의 기본값=4)
):
    """
    파라미터화된 수능 문제 솔버
    
    핵심 관계식:
    - x≥2 구간: (0, b-5]의 자연수 개수 = b-5
    - x<2 구간: (a-interval_width, a)의 자연수 개수 = interval_width - 1
    - 합: (b - 5) + (interval_width - 1) = target_natural_count
    
    최솟값 조건: a ≥ b - 1 → a = b - 1
    
    매개변수:
    - target_natural_count: 조건 나의 자연수 개수 (기본 6)
    - interval_width: (a-δ, a)의 폭 (기본 4)
    
    반환: a + b
    """
    
    a, b = symbols('a b', integer=True, positive=True)
    
    # 자연수 개수 = interval_width - 1
    interval_count = interval_width - 1
    
    # 핵심 관계식: (b - 5) + interval_count = target_natural_count
    eq1 = Eq(b - 5 + interval_count, target_natural_count)
    
    # b 해결
    b_val = sp_solve(eq1, b)[0]
    
    # 최솟값 조건: a = b - 1
    a_val = b_val - 1
    
    # 조건 검증: b ≥ 6 (치역이 {0,1,2}이기 위함)
    if b_val < 6:
        raise ValueError(f'b={b_val} < 6: 조건을 만족하지 않음')
    
    # a + b 반환
    return a_val + b_val


# 원문제 검증
CANDIDATE = 15
print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')