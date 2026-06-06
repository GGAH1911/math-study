from fractions import Fraction
from itertools import product

def solve(cards=[1, 2, 3, 4], num_trials=4, threshold=0):
    """
    카드를 num_trials번 뽑아 점 P를 이동시킨다.
    - 홀수 카드 k: +k 이동
    - 짝수 카드 k: -k 이동
    
    사건 A: 뽑은 카드들의 곱이 홀수 (⟺ 모든 카드가 홀수)
    사건 B: 최종 좌표 S >= threshold
    
    Parameters:
    - cards: 카드 목록 (default: [1, 2, 3, 4])
    - num_trials: 반복 횟수 (default: 4)
    - threshold: 최종 좌표의 최소값 (default: 0)
    
    Returns: P(A|B)의 기약분수 (분자/분모)에서 분모+분자
    """
    odd_cards = {c for c in cards if c % 2 == 1}
    count_B = 0
    count_A_and_B = 0
    
    for combination in product(cards, repeat=num_trials):
        final_coord = sum(card if card % 2 == 1 else -card for card in combination)
        
        if final_coord >= threshold:
            count_B += 1
            if all(card in odd_cards for card in combination):
                count_A_and_B += 1
    
    prob = Fraction(count_A_and_B, count_B)
    return prob.denominator + prob.numerator


CANDIDATE = 61
print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')