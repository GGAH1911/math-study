from fractions import Fraction
from itertools import product

def solve(num_coins=5, initial_heads_count=2, num_rolls=3):
    """
    동전 뒤집기 문제 솔버
    
    Parameters:
    - num_coins: 동전 개수
    - initial_heads_count: 초기 앞면 개수 (첫 initial_heads_count개가 앞)
    - num_rolls: 주사위 던지기 횟수
    
    Returns:
    - p + q (여기서 확률 = q/p, gcd(p,q)=1)
    """
    
    # 초기 상태: 0~(initial_heads_count-1)이 앞(1), 나머지가 뒷(0)
    initial = [1] * initial_heads_count + [0] * (num_coins - initial_heads_count)
    
    # 목표: 모두 앞(1)
    target = [1] * num_coins
    
    valid_count = 0
    total_count = 0
    
    # 주사위를 num_rolls번 던지는 모든 경우
    for rolls in product(range(1, 7), repeat=num_rolls):
        state = initial[:]
        
        # 각 주사위 결과에 따라 동전 뒤집음
        for die_result in rolls:
            if die_result == 6:
                # 모든 동전 뒤집음
                state = [1 - s for s in state]
            elif die_result <= num_coins:
                # 위치 die_result-1 (0-indexed)의 동전 뒤집음
                state[die_result - 1] = 1 - state[die_result - 1]
            # else: die_result > num_coins이고 != 6인 경우 아무것도 하지 않음
        
        total_count += 1
        
        # 모두 앞이면 카운트
        if state == target:
            valid_count += 1
    
    # 확률 계산 (q/p 형태로)
    prob = Fraction(valid_count, total_count)
    q = prob.numerator
    p = prob.denominator
    
    return p + q

# 검증
CANDIDATE = 19
if solve() == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')