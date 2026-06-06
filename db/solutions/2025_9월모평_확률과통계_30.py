# 경우의 수를 직접 계산하여 검증
count = 0

for a_white in range(5):  # A가 받는 흰 공 (0-4)
    for a_black in range(5):  # A가 받는 검은 공 (0-4)
        a_total = a_white + a_black
        
        # 조건 (가): A가 받는 공은 0개, 1개, 2개
        if a_total > 2:
            continue
        
        # 남은 공
        w_remain = 4 - a_white
        b_remain = 4 - a_black
        
        # B와 C에게 분배
        for b_white in range(w_remain + 1):
            for b_black in range(b_remain + 1):
                b_total = b_white + b_black
                
                # 조건 (나): B가 받는 공은 2개 이상
                if b_total >= 2:
                    count += 1

if count == 93:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}, expected 93')