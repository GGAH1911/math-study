import math

# 세 가지 a_1 값 검증
for a1 in [27, 237, 69]:
    seq = [a1]
    for i in range(1, 7):
        an = seq[-1]
        log_base3 = math.log(an) / math.log(3)
        # log_3(an)이 자연수인지 확인 (부동소수점 오차 고려)
        is_natural = abs(log_base3 - round(log_base3)) < 1e-9 and round(log_base3) >= 1
        if is_natural:
            next_a = an / 3
        else:
            next_a = an + 6
        seq.append(int(next_a))
    
    # a_4 ~ a_7의 합 확인
    sum_4_to_7 = sum(seq[3:7])  # index 3~6은 a_4~a_7
    if sum_4_to_7 != 40:
        print(f'VERIFY_FAIL')
        exit()

print('VERIFY_PASS')