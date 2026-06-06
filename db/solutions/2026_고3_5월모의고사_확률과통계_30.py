from itertools import combinations, product
from collections import Counter

# 카드: {1,2,4,8}, 공: 8개 총합
# 조건 (가): 1번 상자 카드 개수 = 1, 8번 상자 카드 개수 >= 2
# 조건 (나): 2번(2의배수 카드|공>=2), 4번(4의배수|공>=4), 8번(8|공>=8)

cards = [1, 2, 4, 8]
count = 0

# 4개 카드를 4개 상자에 배치 (각 카드는 하나의 상자에만 들어감)
for card_assignment in product(range(4), repeat=4):  # card_assignment[i] = 카드 i가 어느 상자에 들어갈지
    # card_assignment[0] = 카드1의 상자, [1] = 카드2의 상자, ...
    
    # 각 상자마다 카드 개수
    box_cards = [list() for _ in range(4)]
    for card_idx, box_idx in enumerate(card_assignment):
        box_cards[box_idx].append(cards[card_idx])
    
    # 조건 (가) 확인
    if len(box_cards[0]) != 1 or len(box_cards[3]) < 2:
        continue
    
    # 공 배치: a+b+d+c=8 (1번, 2번, 4번, 8번)
    # b,d,c >= 0
    for balls_dist in product(range(9), repeat=4):
        a, b, d, c = balls_dist
        if a + b + d + c != 8:
            continue
        
        # 조건 (나) 확인
        # 2번: 2의배수({2,4,8}) 카드 있거나 b>=2
        has_2_mult = any(card in box_cards[1] for card in [2, 4, 8])
        if not (has_2_mult or b >= 2):
            continue
        
        # 4번: 4의배수({4,8}) 카드 있거나 d>=4
        has_4_mult = any(card in box_cards[2] for card in [4, 8])
        if not (has_4_mult or d >= 4):
            continue
        
        # 8번: 8({8}) 카드 있거나 c>=8
        has_8 = 8 in box_cards[3]
        if not (has_8 or c >= 8):
            continue
        
        count += 1

if count == 398:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}, expected 398')