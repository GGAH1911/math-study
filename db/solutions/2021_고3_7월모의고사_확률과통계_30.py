def solve(black_total=4, white_total=5, red_total=5):
    """
    네 명의 학생 A, B, C, D에게 공을 나누어주는 경우의 수
    
    조건:
    (가) 각 학생이 받는 공의 색의 종류의 수는 2
    (나) 학생 A는 흰 공과 검은 공을 받으며 흰 공보다 검은 공을 더 많이 받는다
    (다) 학생 A가 받는 공의 개수는 홀수이며 A가 받는 개수 이상의 공을 받는 학생은 없다
    
    Parameters:
    - black_total: 검은 공 총 개수 (기본값 4)
    - white_total: 흰 공 총 개수 (기본값 5)
    - red_total: 빨간 공 총 개수 (기본값 5)
    
    Returns:
    - 조건을 만족하는 경우의 수
    """
    count = 0
    
    # A가 받을 (검, 흰) 조합
    for a_black in range(1, black_total + 1):
        for a_white in range(1, white_total + 1):
            # 조건 (나): 검 > 흰
            if a_black <= a_white:
                continue
            
            n = a_black + a_white
            
            # 조건 (다): 홀수
            if n % 2 == 0:
                continue
            
            rem_black = black_total - a_black
            rem_white = white_total - a_white
            rem_red = red_total
            
            # B, C, D 분배
            for b_black in range(rem_black + 1):
                for b_white in range(rem_white + 1):
                    for b_red in range(rem_red + 1):
                        b_total = b_black + b_white + b_red
                        b_colors = (b_black > 0) + (b_white > 0) + (b_red > 0)
                        
                        # B의 조건 확인
                        if b_total == 0 or b_total >= n or b_colors != 2:
                            continue
                        
                        for c_black in range(rem_black - b_black + 1):
                            for c_white in range(rem_white - b_white + 1):
                                for c_red in range(rem_red - b_red + 1):
                                    c_total = c_black + c_white + c_red
                                    c_colors = (c_black > 0) + (c_white > 0) + (c_red > 0)
                                    
                                    # C의 조건 확인
                                    if c_total == 0 or c_total >= n or c_colors != 2:
                                        continue
                                    
                                    # D 자동 결정
                                    d_black = rem_black - b_black - c_black
                                    d_white = rem_white - b_white - c_white
                                    d_red = rem_red - b_red - c_red
                                    d_total = d_black + d_white + d_red
                                    d_colors = (d_black > 0) + (d_white > 0) + (d_red > 0)
                                    
                                    # D의 조건 확인
                                    if d_total == 0 or d_total >= n or d_colors != 2:
                                        continue
                                    
                                    count += 1
    
    return count


CANDIDATE = 51
print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')