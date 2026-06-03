def verify():
    # 재귀 관계식 정의
    def next_term(a_n):
        if a_n < 7:
            return 2 * a_n
        else:
            return a_n - 7
    
    # 수열 생성
    sequence = [1]  # a_1 = 1
    for i in range(7):  # a_2부터 a_8까지
        sequence.append(next_term(sequence[-1]))
    
    # 합 계산
    total_sum = sum(sequence)
    
    # 기댓값 검증
    expected = 30
    if total_sum == expected:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: got {total_sum}, expected {expected}')

verify()