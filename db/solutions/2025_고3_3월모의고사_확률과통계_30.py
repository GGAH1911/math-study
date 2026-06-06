from itertools import combinations_with_replacement as cwr

count = 0

# E가 받는 1개 공
for b_E in range(2):  # 0 또는 1
    w_E = 1 - b_E  # 흰공 1-b_E개
    
    # D가 받는 2개 공
    for b_D in range(3):  # 0, 1, 2
        w_D = 2 - b_D  # 흰공 2-b_D개
        
        # A, B, C가 받을 공의 개수
        a_A_plus_B_plus_C = 8 - 1 - 2  # 5개
        black_left = 4 - b_E - b_D
        white_left = 4 - w_E - w_D
        
        # 조건 (가) 확인: A+B+C의 공 개수 합이 홀수
        if a_A_plus_B_plus_C % 2 == 1:
            # A, B, C에게 black_left개 검은공 배분: stars and bars
            ways_black = (black_left + 2) * (black_left + 1) // 2
            # A, B, C에게 white_left개 흰공 배분
            ways_white = (white_left + 2) * (white_left + 1) // 2
            
            count += ways_black * ways_white

if count == 330:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')