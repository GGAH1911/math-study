from sympy import Rational
from itertools import combinations

def solve(
    A_cards=[1, 2, 3, 4],
    B_cards=[2, 3, 4, 5],
    dice_faces=6,
    multiple_of=3,
    cards_if_multiple=(2, 2),
    cards_if_not_multiple=(1, 1),
    target_number=4,
    target_count=2
):
    """
    주머니에서 카드 꺼내기 조건부 확률 솔버
    
    조건:
    - 주사위를 던져 n 획득
    - n이 multiple_of의 배수면: A에서 cards_if_multiple[0]장, B에서 cards_if_multiple[1]장
    - n이 multiple_of의 배수 아니면: A에서 cards_if_not_multiple[0]장, B에서 cards_if_not_multiple[1]장
    
    사건:
    - E: 꺼낸 카드 중 같은 숫자 존재
    - F: 꺼낸 카드 중 target_number가 정확히 target_count개
    
    구하는 값:
    - P(F|E) = p/q (기약분수) → return p+q
    """
    
    A = list(A_cards)
    B = list(B_cards)
    
    # 주사위에서 multiple_of의 배수 개수
    multiple_count = dice_faces // multiple_of
    P_case1 = Rational(multiple_count, dice_faces)
    P_case2 = 1 - P_case1
    
    cards_A_case1, cards_B_case1 = cards_if_multiple
    cards_A_case2, cards_B_case2 = cards_if_not_multiple
    
    # ===== Case 1: n이 multiple_of의 배수 =====
    case1_A_outcomes = list(combinations(A, cards_A_case1))
    case1_B_outcomes = list(combinations(B, cards_B_case1))
    total_case1 = len(case1_A_outcomes) * len(case1_B_outcomes)
    
    E_count_case1 = 0
    FE_count_case1 = 0
    
    for a_combo in case1_A_outcomes:
        for b_combo in case1_B_outcomes:
            a_set = set(a_combo)
            b_set = set(b_combo)
            
            # E 조건: 공통 숫자 존재
            has_common = bool(a_set & b_set)
            if has_common:
                E_count_case1 += 1
                
                # F 조건: target_number가 정확히 target_count개
                count = 0
                if target_number in a_set:
                    count += 1
                if target_number in b_set:
                    count += 1
                
                if count == target_count:
                    FE_count_case1 += 1
    
    P_E_given_case1 = Rational(E_count_case1, total_case1) if total_case1 > 0 else Rational(0)
    P_FE_given_case1 = Rational(FE_count_case1, total_case1) if total_case1 > 0 else Rational(0)
    
    # ===== Case 2: n이 multiple_of의 배수 아님 =====
    case2_A_outcomes = list(combinations(A, cards_A_case2))
    case2_B_outcomes = list(combinations(B, cards_B_case2))
    total_case2 = len(case2_A_outcomes) * len(case2_B_outcomes)
    
    E_count_case2 = 0
    FE_count_case2 = 0
    
    for a_combo in case2_A_outcomes:
        for b_combo in case2_B_outcomes:
            a_set = set(a_combo)
            b_set = set(b_combo)
            
            # E 조건: 공통 숫자 존재
            has_common = bool(a_set & b_set)
            if has_common:
                E_count_case2 += 1
                
                # F 조건: target_number가 정확히 target_count개
                count = 0
                if target_number in a_set:
                    count += 1
                if target_number in b_set:
                    count += 1
                
                if count == target_count:
                    FE_count_case2 += 1
    
    P_E_given_case2 = Rational(E_count_case2, total_case2) if total_case2 > 0 else Rational(0)
    P_FE_given_case2 = Rational(FE_count_case2, total_case2) if total_case2 > 0 else Rational(0)
    
    # ===== 전체 확률 (전체구간 법칙) =====
    P_E = P_E_given_case1 * P_case1 + P_E_given_case2 * P_case2
    P_FE = P_FE_given_case1 * P_case1 + P_FE_given_case2 * P_case2
    
    # ===== 조건부 확률: P(F|E) = P(F∩E) / P(E) =====
    if P_E == 0:
        return None
    
    P_F_given_E = P_FE / P_E
    
    # 기약분수로 표현
    p = P_F_given_E.p
    q = P_F_given_E.q
    
    return p + q


CANDIDATE = 34

if __name__ == "__main__":
    result = solve()
    if result == CANDIDATE:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
        print(f'Expected: {CANDIDATE}, Got: {result}')