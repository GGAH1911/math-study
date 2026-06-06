from sympy import Rational, simplify
from math import comb, gcd

def solve(white_A=3, black_A=1, white_B=3, black_B=1, n_heads=2, n_tails=3, n_draw=5, target_white=2):
    """
    [실행 1]에서 [실행 2] 후 주머니 B에 흰 공이 남아 있지 않을 때,
    [실행 1]에서 주머니 B에 넣은 공 중 흰 공이 target_white개였을 조건부 확률의 분자+분모
    
    Parameters:
    - white_A, black_A: 초기 주머니 A의 흰공, 검은공
    - white_B, black_B: 초기 주머니 B의 흰공, 검은공
    - n_heads: 앞면에서 A에서 꺼내는 공 개수
    - n_tails: 뒷면에서 A에서 꺼내는 공 개수
    - n_draw: 실행 2에서 B에서 꺼내는 공 개수
    - target_white: 구하는 사건 F ([실행 1]에서 흰공 개수)
    """
    
    total_A = white_A + black_A
    total_B = white_B + black_B
    
    P_E = Rational(0)  # 조건 E의 확률: [실행 2] 후 B에 흰 공이 없음
    P_F_cap_E = Rational(0)  # F ∩ E: target_white개 흰공 이동 AND 조건 E
    
    # 앞면 (동전 앞면, 확률 1/2)
    for w in range(min(n_heads, white_A) + 1):
        b = n_heads - w
        if b <= black_A and b >= 0:
            # A에서 (흰w, 검b)을 뽑을 확률
            prob_draw = Rational(comb(white_A, w) * comb(black_A, b), comb(total_A, n_heads))
            
            # 실행 1 후 B의 상태
            B_white = white_B + w
            B_black = black_B + b
            B_total = B_white + B_black
            
            # 실행 2: B에서 n_draw개를 뽑음
            remaining = B_total - n_draw
            
            if remaining >= 0:
                # 남은 공이 모두 검은 공일 확률 (흰공 0개)
                if remaining <= B_black:
                    prob_no_white = Rational(comb(B_black, remaining) * comb(B_white, 0), comb(B_total, remaining))
                else:
                    prob_no_white = Rational(0)
                
                # 이 경우의 기여도
                contribution = Rational(1, 2) * prob_draw * prob_no_white
                P_E += contribution
                
                if w == target_white:
                    P_F_cap_E += contribution
    
    # 뒷면 (동전 뒷면, 확률 1/2)
    for w in range(min(n_tails, white_A) + 1):
        b = n_tails - w
        if b <= black_A and b >= 0:
            # A에서 (흰w, 검b)을 뽑을 확률
            prob_draw = Rational(comb(white_A, w) * comb(black_A, b), comb(total_A, n_tails))
            
            # 실행 1 후 B의 상태
            B_white = white_B + w
            B_black = black_B + b
            B_total = B_white + B_black
            
            # 실행 2: B에서 n_draw개를 뽑음
            remaining = B_total - n_draw
            
            if remaining >= 0:
                # 남은 공이 모두 검은 공일 확률 (흰공 0개)
                if remaining <= B_black:
                    prob_no_white = Rational(comb(B_black, remaining) * comb(B_white, 0), comb(B_total, remaining))
                else:
                    prob_no_white = Rational(0)
                
                # 이 경우의 기여도
                contribution = Rational(1, 2) * prob_draw * prob_no_white
                P_E += contribution
                
                if w == target_white:
                    P_F_cap_E += contribution
    
    # 조건부 확률 계산
    if P_E == 0:
        return None
    
    P_F_given_E = simplify(P_F_cap_E / P_E)
    
    # 기약분수에서 분자(q), 분모(p) 추출
    q = P_F_given_E.p
    p = P_F_given_E.q
    
    # 서로소 확인
    assert gcd(p, q) == 1, f"gcd({p}, {q}) != 1"
    
    return p + q

CANDIDATE = 17
result = solve()
print('VERIFY_PASS' if result == CANDIDATE else 'VERIFY_FAIL')